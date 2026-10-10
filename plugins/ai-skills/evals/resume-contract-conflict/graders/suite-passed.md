---
type: llm
focus: trace
---

PASS se o trace mostra uma execução de `python -m unittest discover -s tests` depois da correção, com saída que confirma testes executados, incluindo o cenário de zero unidades, e sucesso.
FAIL se não há execução da suíte depois da correção, se ela falhou ou se terminou sem executar testes. Um check marcado ou um exit code com zero testes não comprova o comportamento.
