---
description: Preparação de uma mudança para outra sessão, com integração entre contratos existentes e uma política futura ainda ausente.
tags: [plan, prepare, handoff]
max_turns: 100
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
expected_outcome: Plano transferível com dependências e contexto confirmado, checks de integração e recusa atual de pedido pago preservada, sem implementar código.
---

Use a skill sdd para preparar apenas o plano de implementação de `docs/specs/orders/cancel-order/spec.md`. Vou passar a execução para outra sessão, que terá acesso a esses arquivos. Ela precisará entender o contexto de cada item e a ordem das dependências, porque o cancelamento, a autenticação e a consulta usam contratos de componentes diferentes.

Investigue o código disponível, defina as decisões necessárias, organize os resultados implementáveis e suas provas. A política para pedidos pagos continua sem decisão; mantenha a recusa atual e deixe claro o que poderá ser implementado agora e o que depende dessa política. Não implemente o adaptador nem altere o código ou os testes. Copie o plano para `eval-out/plan.md` ao terminar, sem alterar seu conteúdo.
