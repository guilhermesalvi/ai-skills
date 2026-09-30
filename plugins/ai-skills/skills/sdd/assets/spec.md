# {{Nome da capability}}

| | |
| --- | --- |
| **Requirement Prefix** | `{{PREFIXO}}` |
| **Affected Capabilities** | {{Capabilities cujo resultado a mudança altera; apague a linha quando não houver}} |

## Context

{{Problema, consumidor e o trabalho que ele precisa fazer; origem do contrato; código pertinente com arquivo:linha}}

## Scope

{{O que entra e as exclusões que um leitor esperaria ver dentro; apague a seção quando não houver exclusão relevante}}

## Assumptions

- **{{Premissa}}.** {{Origem ou evidência}}. Choice: {{Escolha feita; apague o rótulo quando a premissa não for um default}}. If false: {{Consequência}}. Verified by: {{Quem verifica e como; apague o rótulo quando não for conhecido}}. Confirmed? n

## Gaps

| Gap | Affects | Owner |
| --- | --- | --- |
| {{Informação ou decisão ausente}} | {{IDs ou comportamento que ficam indefinidos}} | {{Quem decide, ou ?}} |

## Glossary

| Term | Identifier | Definition |
| --- | --- | --- |
| {{Termo canônico}} | `{{Identificador no código}}` | {{Definição, com os sinônimos}} |

## Requirements

- **{{PREFIXO}}-01** — {{Requisito, em EARS quando o formato ajudar}}

## Domain Events

| Event | Trigger | Content | Consumers |
| --- | --- | --- | --- |
| `{{Evento}}` | {{Gatilho, com o ID do requisito}} | {{Significado do conteúdo}} | {{Consumidores e o que eles podem assumir}} |

## Acceptance Scenarios

| Scenario | Input | Condition | Requirements | Result |
| --- | --- | --- | --- | --- |
| {{Nome}} | {{Entrada}} | {{Condição}} | {{IDs verificados}} | {{Resultado esperado}} |

## Observable Decisions

| Surface or dimension | Landing |
| --- | --- |
| {{Superfície: decisão; uma linha por decisão de superfície}} | {{Requisito, garantia do código com arquivo:linha, premissa ou lacuna}} |
| Validation and limits | {{Onde está a decisão}} |
| Failure and partial failure | {{Onde está a decisão}} |
| Idempotency and duplication | {{Onde está a decisão}} |
| Authorization | {{Onde está a decisão}} |
| Rate limiting | {{Onde está a decisão}} |
| Concurrency and ordering | {{Onde está a decisão}} |
| Data lifecycle | {{Onde está a decisão}} |
| External dependency failure | {{Onde está a decisão}} |
| State transitions | {{Onde está a decisão}} |
| Observability | {{Onde está a decisão}} |
| Cross-capability consistency | {{Onde está a decisão}} |
| `n/a` | {{Dimensão: motivo, separadas por ponto e vírgula; mova para cá as dimensões que não se aplicam e apague a linha delas acima}} |

## Trade-offs

| Decision | Cost | Reason |
| --- | --- | --- |
| {{Decisão de comportamento, com os IDs}} | {{O que se perde e para quem}} | {{Motivo informado, ou que ninguém o informou}} |

## Divergences

- {{Diferença entre a implementação e a intenção documentada, com arquivo:linha; apague a seção quando a origem não for código}}

## References

- {{Fonte externa ou norma, com link, escopo e data da consulta; apague a seção quando não houver}}
