# Modos condicionais

Use apenas o modo aplicável.

## PRD reverso

Ao documentar o produto existente, derive comportamento de código, testes, documentação e observação. Na análise, distinga comportamento observado de intenção planejada e relate divergências na entrega da revisão. Descreva o resultado para o consumidor em todo o documento, mesmo quando a evidência vier de detalhes de implementação.

Uma intenção não registrada é `[ASSUMPTION]`, com a evidência que motivou a inferência. Um comportamento sem justificativa identificável é uma lacuna de explicação, não prova de que deve ser removido. Se várias intenções forem plausíveis, registre-as em Open Questions; não invente coerência.

Não peça informação que o repositório já fornece. Inspecione primeiro o caminho pertinente e pergunte apenas pelo contexto indispensável que continuar ausente. Não reescreva o produto para fazê-lo concordar com uma justificativa inferida.

## Produto para outros times ou sistemas

Em plataformas, infraestrutura, SDKs e APIs como produto, o usuário é o time ou sistema consumidor. Descreva seu trabalho e resultado esperado, como integrar autenticação sem administrar sessões.

Métricas podem incluir percentis de latência, taxa de erro, adoção, tempo de integração e esforço operacional. Defina limites apenas quando houver fonte ou decisão; resultados de negócio dos consumidores são efeitos indiretos.

Os critérios de aceitação incluem o contrato público pertinente: compatibilidade, estabilidade da interface, disponibilidade e prazo de transição. Quando houver substituição de interface, registre o que deixa de ser atendido, o custo de migração, os consumidores e o cronograma efetivamente decidido. Sem decisão de prazo, identifique a pendência em vez de prometer uma data.
