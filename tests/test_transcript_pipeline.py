"""Exercise file contracts at the split/worker/merge boundary."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "ai-skills" / "skills" / "transcript-fix" / "scripts"


class TranscriptPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.work = self.root / "work"
        self.out = self.root / "output"

    def run_script(self, script, *args):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPTS / script), *map(str, args)],
            cwd=self.root, capture_output=True, text=True, encoding="utf-8",
        )

    def split(self, text, suffix="txt", *options):
        source = self.root / ("source." + suffix)
        source.write_text(text, encoding="utf-8")
        result = self.run_script("split_transcript.py", source, "--out", self.work, *options)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads((self.work / "manifest.json").read_text(encoding="utf-8"))

    def complete_workers(self, manifest):
        fixed = self.work / "fixed"
        fixed.mkdir()
        for chunk in manifest["chunks"]:
            (fixed / f"{chunk['id']:02d}.txt").write_text(
                Path(chunk["file"]).read_text(encoding="utf-8"), encoding="utf-8",
            )
            (fixed / f"{chunk['id']:02d}.changes.json").write_text("[]", encoding="utf-8")

    def merge(self):
        result = self.run_script("merge_chunks.py", "--work", self.work, "--out", self.out, "--name", "lesson")
        report = json.loads((self.out / "lesson.report.json").read_text(encoding="utf-8"))
        return result, report

    def test_plain_text_round_trip_preserves_every_word(self):
        text = " ".join(f"palavra{i}." for i in range(70))
        manifest = self.split(text, "txt", "--words", 20, "--context-words", 12)
        self.complete_workers(manifest)
        result, report = self.merge()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(report["ok"])
        self.assertEqual((self.out / "lesson.fixed.txt").read_text(encoding="utf-8").split(), text.split())

    def test_srt_round_trip_keeps_unicode_and_timestamps(self):
        manifest = self.split("1\n00:00:01,000 --> 00:00:02,000\nOlá, integração.\n\n2\n00:00:03,000 --> 00:00:04,000\nPróxima questão.\n", "srt")
        self.complete_workers(manifest)
        result, report = self.merge()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["chunks"][0]["timestamps"], {"source": 2, "fixed": 2})
        self.assertIn("[00:00:01] Olá, integração.", (self.out / "lesson.fixed.txt").read_text(encoding="utf-8"))

    def test_vtt_accepts_timestamps_without_hour_component(self):
        manifest = self.split("WEBVTT\n\n00:01.000 --> 00:02.000\nOlá mundo.\n\n00:00:03.000 --> 00:00:04.000\nOutra frase.\n", "vtt")
        self.complete_workers(manifest)
        result, report = self.merge()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(report["chunks"][0]["timestamps"]["source"], 2)

    def test_changed_timestamp_fails_even_when_count_is_preserved(self):
        manifest = self.split("1\n00:00:01,000 --> 00:00:02,000\nOlá mundo.\n", "srt")
        self.complete_workers(manifest)
        (self.work / "fixed/00.txt").write_text("[00:00:09] Olá mundo.\n", encoding="utf-8")
        result, report = self.merge()
        self.assertEqual(result.returncode, 1)
        self.assertIn("timestamps", report["chunks"][0]["problems"])

    def test_missing_worker_result_fails(self):
        self.split("Texto completo.")
        result, report = self.merge()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(report["ok"])
        self.assertIn("missing", report["chunks"][0]["problems"])

    def test_truncated_result_fails(self):
        manifest = self.split(" ".join(f"palavra{i}" for i in range(50)))
        self.complete_workers(manifest)
        (self.work / "fixed/00.txt").write_text("Uma frase.", encoding="utf-8")
        result, report = self.merge()
        self.assertEqual(result.returncode, 1)
        self.assertIn("drift", report["chunks"][0]["problems"])

    def test_missing_change_log_fails(self):
        manifest = self.split("Texto completo.")
        self.complete_workers(manifest)
        (self.work / "fixed/00.changes.json").unlink()
        result, report = self.merge()
        self.assertEqual(result.returncode, 1)
        self.assertIn("changes_missing", report["chunks"][0]["problems"])

    def test_invalid_change_logs_are_reported_without_crashing(self):
        manifest = self.split("Texto completo.")
        self.complete_workers(manifest)
        for invalid in ('{', '{}', '[1]', '[{"original":"x","corrected":"y","evidence":"A","count":true}]'):
            with self.subTest(invalid=invalid):
                (self.work / "fixed/00.changes.json").write_text(invalid, encoding="utf-8")
                result, report = self.merge()
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("changes_json_invalid", report["chunks"][0]["problems"])

    def test_zero_context_does_not_copy_the_previous_chunk(self):
        manifest = self.split("Um dois. Três quatro.", "txt", "--words", 2, "--context-words", 0)
        self.assertEqual(len(manifest["chunks"]), 2)
        self.assertTrue(all(c["context_file"] is None for c in manifest["chunks"]))

    def test_empty_input_and_invalid_sizes_are_rejected_before_writing(self):
        source = self.root / "source.txt"
        source.write_text("", encoding="utf-8")
        for options in ([], ["--words", "0"], ["--context-words", "-1"]):
            with self.subTest(options=options):
                result = self.run_script("split_transcript.py", source, "--out", self.work, *options)
                self.assertEqual(result.returncode, 2)
                self.assertFalse((self.work / "manifest.json").exists())

    def test_empty_manifest_cannot_pass_validation(self):
        self.work.mkdir()
        (self.work / "manifest.json").write_text(json.dumps({"chunks": [], "source_words": 0}), encoding="utf-8")
        result, report = self.merge()
        self.assertEqual(result.returncode, 1)
        self.assertIn("empty_manifest", report["problems"])

    def prepare_glossary_batch(self):
        glossary = self.root / "glossary.json"
        candidates = self.root / "candidates.json"
        receipt = self.root / "merge.json"
        glossary.write_text("[]", encoding="utf-8")
        candidates.write_text(json.dumps([{
            "correct": "trade-off", "variants": ["tredófi"],
            "evidence": "A", "occurrences": 3, "example": "um tredófi",
        }]), encoding="utf-8")
        return glossary, candidates, receipt

    def merge_glossary(self, glossary, candidates, receipt):
        return self.run_script("glossary_tool.py", "merge", "--glossary", glossary,
                               "--candidates", candidates, "--receipt", receipt)

    def test_replaying_a_batch_does_not_double_counts(self):
        paths = self.prepare_glossary_batch()
        for _ in range(2):
            result = self.merge_glossary(*paths)
            self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads(paths[0].read_text(encoding="utf-8"))
        self.assertEqual(entries[0]["occurrences"], 3)
        self.assertFalse(entries[0]["confirmed"])

    def test_prepared_receipt_recovers_interrupted_glossary_publication(self):
        paths = self.prepare_glossary_batch()
        self.assertEqual(self.merge_glossary(*paths).returncode, 0)
        record = json.loads(paths[2].read_text(encoding="utf-8"))
        # Recreate the state after receipt publication but before glossary replacement.
        paths[0].write_text(json.dumps(record["before"]), encoding="utf-8")
        result = self.merge_glossary(*paths)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(paths[0].read_text(encoding="utf-8")), record["after"])

    def test_stale_batch_cannot_overwrite_later_glossary_changes(self):
        paths = self.prepare_glossary_batch()
        self.assertEqual(self.merge_glossary(*paths).returncode, 0)
        entries = json.loads(paths[0].read_text(encoding="utf-8"))
        entries[0]["confirmed"] = True
        paths[0].write_text(json.dumps(entries), encoding="utf-8")
        before = paths[0].read_bytes()
        result = self.merge_glossary(*paths)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(paths[0].read_bytes(), before)

    def test_contextual_uncertainty_is_not_forced_into_global_mapping(self):
        glossary, candidates, receipt = self.prepare_glossary_batch()
        self.assertEqual(self.merge_glossary(glossary, candidates, receipt).returncode, 0)
        transcript = self.root / "fixed.txt"
        for text, expected in (("Um tredófi [?] neste contexto.", 0), ("Um tredófi neste contexto.", 1)):
            with self.subTest(text=text):
                transcript.write_text(text, encoding="utf-8")
                result = self.run_script("check_consistency.py", "--glossary", glossary, "--text", transcript)
                self.assertEqual(result.returncode, expected, result.stdout)


if __name__ == "__main__":
    unittest.main()
