# Decisão arquitetural

Use ADR para uma escolha que define convenção, restrição ou padrão para outras capabilities: estilo arquitetural, transporte de eventos ou política de versionamento, por exemplo. Uma decisão local permanece em Technical Decisions do plano da mudança; se o pedido for um ADR para ela, diga em uma linha que ela caberia no plano e escreva o ADR.

Registrar uma decisão não amplia o escopo: aplicá-la ao restante do projeto exige pedido próprio.

## Conteúdo e destino

Preserve o motivo, as alternativas realmente avaliadas, os benefícios e os custos aceitos. Registre os participantes conhecidos, sem inventar nomes. Um custo genérico que se aplica a qualquer solução não explica a escolha.

Use `docs/adr/NNNN-<decisão>.md`. Preserve o formato dos ADRs existentes; sem ADR anterior, use a estrutura abaixo.

| Section | Conteúdo |
| --- | --- |
| Título | `ADR NNNN: <decisão>` |
| Participants | Quem decidiu ou foi consultado, quando conhecido |
| Context | Problema, restrições e critérios |
| Decision | Escolha e seu alcance |
| Alternatives Considered | Alternativas reais avaliadas pelos mesmos critérios e motivo da rejeição |
| Consequences | Benefícios e custos concretos aceitos |
| Derived Rules | Regras criadas ou alteradas, com link para o arquivo onde cada uma é mantida |

Derived Rules só existe quando a decisão cria ou altera uma regra. Mantenha cada regra no arquivo responsável pelo objeto que ela governa, e acrescente a essa regra o vínculo com o ADR que a justifica.

## ADR avulso

Fora de um plano, leia os ADRs vigentes e as specs e o código que a decisão atinge, para achar conflitos e as capabilities afetadas.

Se o pedido não indicar a escolha, compare as alternativas pelos mesmos critérios, recomende uma e peça a escolha ao usuário antes de escrever: o ADR registra a decisão, não a recomendação.

Ao registrar uma decisão já adotada no código, derive contexto e decisão do código, dos commits e da documentação, e marque como inferência o motivo que a evidência não mostra. Quando ninguém registrou as alternativas avaliadas ou os participantes, diga isso nas seções correspondentes em vez de reconstruí-los.

## Cumprir ou substituir uma decisão

Leia os ADRs pertinentes antes de planejar. Quando uma escolha conflitar com um ADR vigente, explicite se a solução seguirá a restrição ou se é necessária sua substituição, dentro da autorização do pedido.

Ao substituir, crie o novo ADR com `Supersedes: NNNN` e acrescente `Superseded by: NNNN` ao anterior. Preserve o conteúdo histórico do documento antigo e confira que as referências são recíprocas e apontam para arquivos existentes.
