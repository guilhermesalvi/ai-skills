---
description: Implementação de um plano existente, com testes a criar, checks a marcar e verificação no fim. Precisa de Bash para executar os testes.
tags: [implement, needs-bash]
plugins: ["../.."]
max_turns: 120
timeout_seconds: 2400
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
expected_outcome: cancel implementado com os testes nomeados no plano, todos os checks marcados depois de executados, e um relatório de verificação.
---

Implemente o plano docs/specs/order-lifecycle/0001-customer-cancellation.md.
