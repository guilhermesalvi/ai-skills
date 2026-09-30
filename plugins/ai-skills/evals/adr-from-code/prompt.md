---
description: ADR de uma decisão já adotada no código, sem registro de quem decidiu nem das alternativas.
tags: [adr]
plugins: ["../.."]
max_turns: 50
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
expected_outcome: Um ADR 0001 derivado do código e dos commits, que não inventa participantes, alternativas avaliadas nem motivo.
---

Registre num ADR a decisão de guardar todos os instantes em UTC, que o código já segue.

Quando terminar, copie o ADR para `eval-out/adr.md`, sem alterar o conteúdo.
