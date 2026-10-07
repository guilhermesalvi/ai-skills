# Decisão arquitetural

Registre uma decisão que vale para múltiplas capabilities.

## Alcance

- Se o pedido for um ADR para uma decisão que vale só para uma capability, indique onde ela caberia e escreva o ADR mesmo assim: em Technical Decisions do plano, numa mudança em andamento, ou junto do código, numa decisão já adotada.
- Registrar uma decisão não autoriza mudanças nas capabilities que ela alcança. A aplicação da decisão segue o escopo de implementação autorizado pelo usuário.

## Conteúdo

- Preserve o motivo, as alternativas realmente avaliadas, os benefícios e os custos aceitos.
- Registre os participantes conhecidos, sem inventar nomes.
- Um custo genérico, que se aplica a qualquer solução, não explica a escolha.
- Mantenha a definição de cada regra derivada no arquivo responsável pelo contrato, componente ou convenção afetada. Nesse arquivo, vincule a regra ao ADR que a justifica.

## Arquivo e estrutura

- Use `docs/adr/NNNN-<decisão>.md`.
- Preserve o formato dos ADRs existentes no projeto consumidor. Use o modelo da skill quando o projeto ainda não tiver ADRs.
- No formato do modelo, o título é `# ADR NNNN: <decisão>`.
- No formato do modelo, registre as substituições na tabela de cabeçalho logo abaixo do título: Supersedes no ADR novo e Superseded by no ADR substituído.

| Section | Conteúdo |
| --- | --- |
| Participants | Quem decidiu ou foi consultado; ausência de registro quando ninguém for conhecido |
| Context | Problema, restrições, critérios e origem do motivo da escolha |
| Decision | Escolha e seu alcance |
| Alternatives Considered | Alternativas reais avaliadas pelos mesmos critérios e motivo da rejeição |
| Consequences | Benefícios e custos concretos aceitos |
| Derived Rules | Regras criadas ou alteradas, com link para o arquivo onde cada uma é mantida |
| References | Fontes externas consultadas |

- Derived Rules só existe quando a decisão cria ou altera uma regra.
- References só existe quando o ADR se apoia em fonte externa.

## ADR avulso

- Fora de um plano, leia os ADRs vigentes e as specs e o código que a decisão atinge, para achar conflitos e as capabilities afetadas.
- Se a escolha estiver em aberto, compare as alternativas pelos mesmos critérios. Decida quando o usuário tiver delegado essa escolha; caso contrário, recomende uma e peça a decisão antes de registrar o ADR. O documento registra uma escolha adotada, com sua origem.
- Ao registrar uma decisão já adotada no código, derive contexto e decisão do código, dos commits e da documentação.
- Separe a escolha observada do motivo histórico. Se o código mostrar a escolha, mas nenhuma fonte registrar por que ela foi adotada, declare em Context: "O motivo original não está registrado." Apresente uma explicação provável como inferência, por exemplo, "Infere-se que a escolha evita..."; um benefício técnico plausível não comprova a intenção original.
- Quando ninguém registrou as alternativas avaliadas ou os participantes, diga isso nas seções correspondentes em vez de reconstruí-los.

## Substituir uma decisão

- Crie o ADR substituto com `Supersedes` no cabeçalho, apontando para o ADR substituído.
- Acrescente `Superseded by` ao cabeçalho do ADR substituído, apontando para o ADR substituto.
- Preserve o conteúdo histórico do documento antigo.
- Confira que as referências são recíprocas e apontam para arquivos existentes.
