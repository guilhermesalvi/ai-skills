# Plano

Produza um plano que outro executor consiga seguir sem adivinhar decisões nem o que provar. O plano decide como cumprir a spec, com profundidade proporcional ao risco, e fixa os checks: as afirmações que a mudança precisa tornar verdadeiras, cada uma com a prova que a decide.

O plano não decompõe o trabalho em tarefas. Ordem, arquivos e divisão em passos ficam com quem implementa e aparecem no diff: granularidade compra ordem, não correção, e um roteiro a obedecer disputa atenção com as obrigações.

## Contexto pertinente

Leia a spec, os ADRs que restringem a mudança e o código que ela atinge, não o repositório inteiro: siga do contrato público para as implementações necessárias. Registre o que foi inspecionado e as limitações relevantes. Nunca exponha segredos ou dados pessoais ao citar evidência.

Distinga o peso de cada fonte: uma regra escrita é convenção, enquanto um padrão inferido de poucos exemplos é hipótese. Para componentes novos, identifique o que será reutilizado e por que outra estrutura é necessária.

Problemas adjacentes entram no plano quando afetarem uma decisão; eles não expandem o escopo.

## Decisões técnicas

Registre as escolhas que outro executor não deduziria da spec e do código.

Defina os critérios antes de comparar soluções, a partir dos requisitos, ADRs, restrições, custo e prazo. Um critério descreve qualidade ou limite, não o mecanismo preferido; confira se falta algum que poderia inverter a escolha. Compare alternativas reais pelo mesmo escopo e pelos mesmos critérios, e escolha a que atende ao contrato com custo e risco justificáveis. Se não houver alternativa materialmente viável, registre o motivo em vez de inventar opções.

Rejeite uma alternativa pela propriedade que a desqualifica, como “não expressa o próximo estado”, e não por preferência, como “mais limpo”, que ninguém consegue contestar. Confira se uma solução mais simples ou menos arriscada também satisfaz o contrato.

Use a arquitetura do projeto quando ela atende ao problema. Módulo de código, pacote versionado e unidade que sobe e desce em conjunto são decisões distintas: avalie primeiro uma mudança no serviço existente, depois um módulo interno e, só com necessidade concreta de isolamento, escala ou cadência, uma nova unidade implantável, com dono, operação, contrato e compatibilidade. Uma biblioteca compartilhada precisa de dono, consumidores e estabilidade suficiente; não extraia regras de negócio para ela apenas por semelhança de código.

Uma decisão que define convenção, restrição ou padrão para outras capabilities, como estilo arquitetural, transporte de eventos ou política de versionamento, vai para [ADR](adr.md), dentro da autorização existente; decisões locais ficam no plano.

Quando uma escolha conflitar com um ADR vigente, explicite se a solução seguirá a restrição ou se o ADR precisa ser substituído, dentro da autorização do pedido; a substituição segue o [ADR](adr.md).

Cada garantia negativa da spec em escopo, como não duplicar nem cobrar duas vezes, tem aqui o mecanismo que a sustenta, a menos que a spec cite um mecanismo que o código já oferece.

Marque como irreversível, com o motivo, a decisão cujo desfazer custa mais que uma refatoração: esquema persistido, contrato que outro consome, dependência nova de runtime, migração sobre dados existentes ou precedente que o repositório ainda não tem. Registre em Choice a forma literal que o próximo leitor vai copiar, como a definição do índice, o valor do enum ou a versão do pacote, e em Reversible o motivo do `Não`. Escopo adiado e regra sem mecanismo se desfazem sem esse custo e não entram.

## Estrutura e riscos

Em Structure, descreva o caminho da mudança pelos componentes existentes e novos, um salto por linha, e, se houver persistência, entidades, relações, invariantes e migração. Contratos entre componentes entram quando outro executor não os deduziria, e também a ordem de operações que sustenta a correção, como travar antes de avaliar. Pasta, nome de arquivo, colunas fora de uma forma literal e divisão em classes ficam com a convenção do repositório e com o diff: um catálogo de caminhos envelhece e engana o próximo leitor.

Para cada evento, registre o transporte, a ordenação e a evolução de versão. A garantia de entrega vem do transporte escolhido: não presuma entrega exatamente uma vez, e descreva como duplicações e falhas são tratadas.

Registre os riscos concretos da mudança, cada um com mitigação, evidência ou aceitação justificada. A tabela sugere técnicas a avaliar, não escolhas obrigatórias.

| Risco | Técnicas a avaliar conforme o contrato |
| --- | --- |
| Evento perdido ou estado inconsistente | Contrato de entrega, consistência e publicação transacional ou equivalente |
| Concorrência, repetição ou reordenação | Chave de idempotência, controle de versão, restrição de unicidade, transições explícitas |
| Integração instável | Isolamento do contrato, timeout, política de repetição e tratamento de indisponibilidade |
| Cálculo financeiro | Precisão, arredondamento e regras isoladas com cenários numéricos |
| Migração ou incompatibilidade | Sequência de transição, compatibilidade e recuperação |
| Desempenho | Orçamento medido, paginação e índices pertinentes |
| Dados regulados ou autorização | Fronteira de acesso, retenção, auditoria e redução de exposição |

## Checks

Um check é uma afirmação observável com valor concreto e a prova que a decide: o teste ou o comando cujo exit code a resolve, num trecho de código no fim do item. Sem prova, não há check. Num projeto novo, a prova nomeia o teste que a implementação vai criar. Escreva a afirmação a partir da spec e das decisões, nunca a partir de uma implementação existente.

Conheça a verificação do projeto antes de escolher as provas: leia as instruções das áreas atingidas, a documentação de build e testes, a configuração dos projetos e a CI, e os testes pertinentes para entender framework, estilo e camada. Escolha a prova que observa o requisito na camada em que ele é definido; testes de integração, publicação ou mutação entram quando a mudança, a regra local ou o pedido os justifica.

Cada requisito em escopo aparece em algum check pelo ID, e esses IDs já formam a rastreabilidade: não os repita numa tabela à parte. Um requisito que nenhum check prova está fora do escopo declarado ou é lacuna, e precisa de resposta antes da execução. Um requisito que uma lacuna deixa decidido só em parte tem check da parte decidida.

Um requisito sobre um conjunto tem um check por membro nomeado na spec, ou um check que percorre o conjunto inteiro com o tamanho declarado. Cada decisão irreversível tem um check que prova a forma literal. Quando a mudança não precisar de teste novo, o check nomeia a verificação existente que a cobre.

O último check é o gate do repositório, com o comando confirmado na configuração real do projeto. Sem projeto ou sem comando confirmável, o comando provável vai para Assumptions, e o gate entra em Checks quando for confirmado.

Registre no plano o estado inicial dos checks quando ele for necessário para distinguir regressões.

## Estrutura do documento

O título é o nome da mudança. Use as seções pertinentes, nesta ordem; Checks é a base.

| Section | Conteúdo | Forma |
| --- | --- | --- |
| Context | Base de comparação, código inspecionado e limitações que afetam a solução | Parágrafos |
| Technical Decisions | Critérios, quando houver comparação, e as decisões | Parágrafo de critérios e tabela Decision, Choice, Rejected alternatives, Cost, Reversible |
| Structure | Caminho, entidades, relações, invariantes, migração e eventos | Lista ou diagrama |
| Risks | Riscos concretos e sua mitigação, evidência ou aceitação | Tabela Risk, Mitigation |
| Assumptions | Inferências e defaults da solução | Lista, como define o fluxo comum |
| Gaps | Informações e decisões ausentes que a solução precisa | Tabela, como define o fluxo comum |
| Checks | Afirmações com prova | Lista de checkboxes |
| References | Fontes técnicas consultadas, como define o fluxo comum | Lista |

## Exemplo parcial

```markdown
## Technical Decisions

| Decision | Choice | Rejected alternatives | Cost | Reversible |
| --- | --- | --- | --- | --- |
| Ordenação de solicitações | Sequência por livro, com unicidade em `(book_id, sequence)` | Instante informado pelo cliente: não distingue registros com o mesmo horário | Concorrência sobre a geração da sequência | Não: esquema persistido |

## Checks

- [ ] **EXM-01**: repetir chave e conteúdo retorna o resultado original e mantém uma única solicitação — `dotnet test --filter RequestIdempotencyTests.RepeatReturnsOriginal`
- [ ] **EXM-02**: repetir a chave com outro conteúdo retorna conflito e preserva a primeira solicitação — `dotnet test --filter RequestIdempotencyTests.ConflictKeepsFirst`
- [ ] Ordenação de solicitações: a migração cria a unicidade `(book_id, sequence)` — `dotnet test --filter MigrationTests.SequenceIsUnique`
- [ ] Gate: `dotnet build` e `dotnet test` passam — `dotnet build && dotnet test`
```
