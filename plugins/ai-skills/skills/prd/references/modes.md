# Modos condicionais

## PRD reverso

Ao documentar um produto que já existe, derive o comportamento de código, testes, documentação e observação. Inspecione primeiro o caminho pertinente e pergunte apenas pelo contexto indispensável que continuar ausente.

Distinga comportamento observado de intenção planejada, e relate as divergências na entrega da revisão. Descreva o resultado para o consumidor em todo o documento, mesmo quando a evidência vier de detalhes de implementação.

- **Intenção não registrada.** Marque `[ASSUMPTION]` e registre a evidência que motivou a inferência.
- **Comportamento sem justificativa identificável.** É uma lacuna de explicação, não prova de que deve ser removido.
- **Várias intenções plausíveis.** Registre-as em Open Questions em vez de inventar coerência.

Não reescreva o produto para fazê-lo concordar com uma justificativa inferida.

## Produto para outros times ou sistemas

Em plataformas, infraestrutura, SDKs e APIs como produto, o usuário é o time ou o sistema consumidor. Descreva o trabalho dele e o resultado que ele espera, como integrar autenticação sem administrar sessões.

| Seção | Ajuste |
| --- | --- |
| Success Metrics | Percentis de latência, taxa de erro, adoção, tempo de integração e esforço operacional. Resultados de negócio dos consumidores são efeitos indiretos |
| Acceptance Criteria | O contrato público pertinente: compatibilidade, estabilidade da interface, disponibilidade e prazo de transição |
| Substituição de interface | O que deixa de ser atendido, custo de migração, consumidores afetados e cronograma efetivamente decidido |

## Visão geral

Crie o PRD 0000 quando a pasta tiver mais de um PRD de capability. Ele explica propósito, responsabilidades e interações entre contextos, com apenas o detalhe necessário para entendê-las. Invariantes, cálculos, critérios de sucesso, decisões de produto e suas fontes ficam no PRD da capability responsável.

O arquivo se chama `0000-<slug>-overview.md` e tem o marcador `<!-- prd: overview -->` na primeira linha, antes do título. O cabeçalho usa `Scope` no lugar de `Originating Context`, e o documento não tem linha de prefixo nem requisitos.

As seções, nesta ordem e conforme o conteúdo pertinente, são Purpose, Contexts, Event Catalog, Flows Between Contexts, Terms per Context e Decisions Delegated to ADR.

Event Catalog identifica produtores, consumidores, requisitos de recepção e links para os contratos em Domain Events dos PRDs produtores. É o único lugar que liga um evento aos requisitos dos consumidores.

Cada decisão delegada a ADR indica o requisito que precisa satisfazer. Uma decisão arquitetural ainda ausente não vira regra de produto por aparecer na visão geral.
