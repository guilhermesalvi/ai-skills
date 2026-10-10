---
description: Retomada com diff que viola o contrato e checks marcados antes da alteração local.
tags: [execute, verify, resume, needs-bash]
max_turns: 100
timeout_seconds: 1200
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
expected_outcome: Correção do código conforme a spec, preservação do resultado de zero unidades e nova execução dos checks afetados.
---

Use a skill sdd para retomar e concluir a mudança em `docs/specs/unit-validation/0001-accept-zero.md`, verificando a implementação contra a spec e o plano atuais. Preserve o trabalho existente e corrija os achados dentro desse escopo. Não faça commit.
