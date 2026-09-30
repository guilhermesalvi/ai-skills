# Decisão arquitetural

Registre uma decisão que vale para outras capabilities.

## Alcance

- Se o pedido for um ADR para uma decisão que vale só para uma capability, diga em uma linha onde ela caberia e escreva o ADR mesmo assim: em Technical Decisions do plano, numa mudança em andamento, ou junto do código, numa decisão já adotada.
- Registrar uma decisão não amplia o escopo: aplicá-la ao restante do projeto exige pedido próprio.

## Conteúdo

- Preserve o motivo, as alternativas realmente avaliadas, os benefícios e os custos aceitos.
- Registre os participantes conhecidos, sem inventar nomes.
- Um custo genérico, que se aplica a qualquer solução, não explica a escolha.
- Mantenha cada regra derivada no arquivo responsável pelo objeto que ela governa, e acrescente a essa regra o vínculo com o ADR que a justifica.

## Arquivo e estrutura

- Use `docs/adr/NNNN-<decisão>.md`.
- Preserve o formato dos ADRs existentes. O modelo de ADR vale quando não há ADR anterior.
- O título é `# ADR NNNN: <decisão>`.
- Logo abaixo do título, a tabela de cabeçalho traz Supersedes e Superseded by quando houver substituição.

| Section | Conteúdo |
| --- | --- |
| Participants | Quem decidiu ou foi consultado, quando conhecido |
| Context | Problema, restrições e critérios |
| Decision | Escolha e seu alcance |
| Alternatives Considered | Alternativas reais avaliadas pelos mesmos critérios e motivo da rejeição |
| Consequences | Benefícios e custos concretos aceitos |
| Derived Rules | Regras criadas ou alteradas, com link para o arquivo onde cada uma é mantida |
| References | Fontes externas consultadas |

- Derived Rules só existe quando a decisão cria ou altera uma regra.
- References só existe quando o ADR se apoia em fonte externa.

## ADR avulso

- Fora de um plano, leia os ADRs vigentes e as specs e o código que a decisão atinge, para achar conflitos e as capabilities afetadas.
- Se o pedido não indicar a escolha, compare as alternativas pelos mesmos critérios, recomende uma e peça a escolha ao usuário antes de escrever. O ADR registra a decisão, não a recomendação.
- Ao registrar uma decisão já adotada no código, derive contexto e decisão do código, dos commits e da documentação.
- Marque como inferência o motivo que a evidência não mostra.
- Quando ninguém registrou as alternativas avaliadas ou os participantes, diga isso nas seções correspondentes em vez de reconstruí-los.

## Substituir uma decisão

- Crie o novo ADR com `Supersedes` no cabeçalho, apontando para o anterior.
- Acrescente `Superseded by` ao cabeçalho do anterior, apontando para o novo.
- Preserve o conteúdo histórico do documento antigo.
- Confira que as referências são recíprocas e apontam para arquivos existentes.
