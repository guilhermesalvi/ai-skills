# Decisão arquitetural

Use ADR para uma escolha que define convenção, restrição ou padrão para outras capabilities: estilo arquitetural, transporte de eventos ou política de versionamento, por exemplo. Uma decisão local permanece no design da mudança.

Registrar uma decisão não amplia o escopo: aplicá-la ao restante do projeto exige pedido próprio.

## Conteúdo e destino

Preserve o motivo, as alternativas realmente avaliadas, os benefícios e os custos aceitos. Registre os participantes conhecidos, sem inventar nomes. Um custo genérico que se aplica a qualquer solução não explica a escolha.

Use `docs/adr/NNNN-<decisão>.md`. Preserve o formato dos ADRs existentes; sem ADR anterior, use a estrutura abaixo.

| Seção ou campo | Conteúdo |
| --- | --- |
| Título | `ADR NNNN: decisão` |
| Participantes | Quem decidiu ou foi consultado, quando conhecido |
| Contexto | Problema, restrições e critérios |
| Decisão | Escolha e seu alcance |
| Alternativas consideradas | Alternativas reais avaliadas pelos mesmos critérios e motivo da rejeição |
| Consequências | Benefícios e custos concretos aceitos |
| Regras derivadas | Regras criadas ou alteradas, com link para o arquivo onde cada uma é mantida |

Regras derivadas só existe quando a decisão cria ou altera uma regra. Mantenha cada regra no arquivo responsável pelo objeto que ela governa, e acrescente a essa regra o vínculo com o ADR que a justifica.

## Cumprir ou substituir uma decisão

Leia os ADRs pertinentes antes de projetar. Quando uma escolha conflitar com um ADR vigente, explicite se a solução seguirá a restrição ou se é necessária sua substituição, dentro da autorização do pedido.

Ao substituir, crie o novo ADR com `Substitui: NNNN` e acrescente `Substituído por: NNNN` ao anterior. Preserve o conteúdo histórico do documento antigo e confira que as referências são recíprocas e apontam para arquivos existentes.
