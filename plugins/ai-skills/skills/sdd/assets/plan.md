# {{Nome da mudança}}

| | |
| --- | --- |
| **Requirements in Scope** | {{IDs cujo comportamento a mudança cria, altera ou precisa provar, separados por vírgula, ou none quando não houver ID em escopo}} |

## Context

{{Base de comparação, estado dos artefatos usado como entrada, código inspecionado e limitações que afetam a solução}}

## Technical Decisions

{{Critérios, quando houver comparação; apague a seção quando não houver decisão que outro executor não deduziria}}

| Decision | Choice | Rejected alternatives | Cost | Reversible |
| --- | --- | --- | --- | --- |
| {{Decisão}} | {{Escolha, com a forma literal}} | {{Alternativa: propriedade que a desqualifica, ou o motivo de não haver alternativa viável}} | {{Custo}} | {{Sim, ou Não: motivo}} |

## Assumptions

- **{{Premissa ainda aberta, uma por item; apague a seção quando não houver inferência nem escolha provisória}}.** {{Explique em prosa o fundamento, a escolha provisória quando houver, a consequência de estar errada e quem verifica quando conhecido}}.

## Gaps

| Gap | Affects | Owner |
| --- | --- | --- |
| {{Informação ou decisão ausente}} | {{Decisão ou check que fica indefinido}} | {{Quem decide, ou ?; apague a seção quando nada estiver em aberto}} |

## Checks

- [ ] **{{ID}}**: {{Afirmação observável com valor concreto}} — `{{Teste ou comando}}`
- [ ] Gate: {{O que passa}} — `{{Comando do gate}}`
