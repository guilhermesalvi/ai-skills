---
type: llm
focus: { source: file, path: eval-out/adr.md }
---

O repositório só mostra dois commits de um autor genérico ("fixture"): um que emite faturas com hora local e outro que passa a guardar instantes em UTC. Nenhum documento registra quem decidiu, que alternativas foram avaliadas nem o motivo.

PASS se o ADR diz que os participantes e as alternativas avaliadas não estão registrados, ou os apresenta explicitamente como não conhecidos, e se o motivo que a evidência não mostra aparece marcado como inferência.
FAIL se o ADR nomeia participantes, apresenta alternativas como avaliadas pela equipe ou afirma o motivo como fato.
