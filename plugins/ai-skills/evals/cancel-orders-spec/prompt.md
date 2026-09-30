---
description: Pedido vago de funcionalidade num módulo sem spec, com uma decisão de negócio que envolve dinheiro.
tags: [spec, plan]
plugins: ["../.."]
max_turns: 80
timeout_seconds: 1500
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
expected_outcome: Spec da capability do ciclo do pedido, com autorização e concorrência decididas ou registradas, o cancelamento de pedido pago como lacuna, e um plano com Requirements in Scope.
---

Quero que o cliente consiga cancelar pedidos. Escreva a spec e o plano.

Quando terminar, copie a spec para `eval-out/spec.md` e o plano para `eval-out/plan.md`, sem alterar o conteúdo.
