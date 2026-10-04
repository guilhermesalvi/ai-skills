# Plano

Produza um plano que outro executor consiga seguir sem adivinhar decisões nem o que provar. Ajuste a profundidade ao risco da mudança.

Fixe os checks: afirmações que a mudança precisa tornar verdadeiras, cada uma com uma prova capaz de decidir seu resultado.

Conteúdo: O que o plano não faz · Contexto pertinente · Escopo · Decisões técnicas · Structure e eventos · Riscos · Checks · Estrutura do documento · Exemplo parcial

## O que o plano não faz

- Não decomponha o trabalho em tarefas, passos ou lista de arquivos. Ordem, arquivos e divisão ficam com quem implementa e aparecem no diff.

Neste formato, decisões e provas orientam a execução. Uma lista de passos não substitui essas obrigações.

## Contexto pertinente

- Leia a spec, os ADRs que restringem a mudança e o código que ela atinge, não o repositório inteiro. Siga do contrato público para as implementações necessárias.
- Registre em Context o que foi inspecionado e as limitações que afetam a solução.
- Nunca exponha segredos ou dados pessoais ao citar evidência.
- Distinga o peso de cada fonte: uma regra escrita é convenção; um padrão inferido de poucos exemplos é hipótese.
- Para componentes novos, identifique o que será reutilizado e por que outra estrutura é necessária.
- Problemas adjacentes entram no plano quando afetarem uma decisão. Eles não expandem o escopo.

## Escopo

- A tabela de cabeçalho traz Requirements in Scope: os IDs que a mudança cria, altera ou precisa provar, separados por vírgula.
- Use `none` quando a mudança não altera nenhum requisito, como numa refatoração sem mudança observável.
- Um requisito que só registra comportamento existente, sem que a mudança o altere, fica fora do escopo, mesmo quando nasce junto com a spec. O gate continua cobrindo-o.
- Um requisito decidido só em parte entra no escopo, com check da parte decidida.
- Um requisito existente que a mudança amplia sem alterar o texto, como uma recusa que passa a cobrir um estado novo, entra no escopo, com check do caso novo.
- O `check_spec.py` confere que cada ID do escopo tem check e que cada check cita apenas IDs do escopo. Não repita essa rastreabilidade numa tabela à parte.

## Decisões técnicas

### O que registrar

- Registre as escolhas que outro executor não deduziria da spec e do código.
- Cada garantia negativa da spec em escopo tem aqui o mecanismo que a sustenta, a menos que a spec cite um mecanismo que o código já oferece.

### Comparar alternativas

- Defina os critérios antes de comparar soluções, a partir dos requisitos, ADRs, restrições, custo e prazo.
- Um critério descreve qualidade ou limite, não o mecanismo preferido. Confira se falta algum critério que poderia inverter a escolha.
- Compare alternativas reais pelo mesmo escopo e pelos mesmos critérios, e escolha a que atende ao contrato com custo e risco justificáveis.
- Sem alternativa materialmente viável, escreva o motivo em Rejected alternatives em vez de inventar opções.
- Rejeite uma alternativa pela propriedade que a desqualifica, como "não expressa o próximo estado", e não por preferência, como "mais limpo", que ninguém consegue contestar.
- Confira se uma solução mais simples ou menos arriscada também satisfaz o contrato.

### Arquitetura

- Use a arquitetura do projeto quando ela atende ao problema.
- Distinga módulo de código, pacote versionado e unidade implantável. Avalie se a mudança cabe no serviço existente ou num módulo interno. Proponha uma nova unidade implantável quando houver necessidade concreta de isolamento, escala ou cadência, com dono, operação, contrato e compatibilidade definidos.
- Uma biblioteca compartilhada precisa de dono, consumidores e estabilidade suficiente. Não extraia regras de negócio para ela apenas por semelhança de código.
- Uma decisão que define convenção, restrição ou padrão para outras capabilities, como estilo arquitetural, transporte de eventos ou política de versionamento, vai para [ADR](adr.md), dentro da autorização existente. Decisões locais ficam no plano.
- Quando uma escolha conflitar com um ADR vigente, explicite em Technical Decisions se a solução seguirá a restrição ou se o ADR precisa ser substituído. A substituição segue o [ADR](adr.md).

### Decisões irreversíveis

- Marque `Não` em Reversible, com o motivo, quando desfazer a decisão custa mais que uma refatoração:
  - esquema persistido;
  - contrato consumido fora da mudança, inclusive uma API pública cujos chamadores ainda não são conhecidos;
  - dependência nova de runtime;
  - migração sobre dados existentes;
  - precedente que o repositório ainda não tem.
- Registre em Choice a forma literal: o texto exato de uma assinatura, índice, valor de enum ou versão que o executor precisa usar.
- Escopo adiado e regra de negócio sem mecanismo técnico não são decisões irreversíveis, porque se desfazem sem esse custo.

## Structure e eventos

- Reserve Structure para dependências, relações e ordens que outro executor não deduziria da spec, do código e de Technical Decisions. Liste apenas essa informação adicional, um salto por linha; sem ela, remova a seção.
- Inclua entidades, invariantes e migração quando a mudança as exigir e os demais registros ainda não as definirem.
- Não liste pastas, nomes de arquivo, colunas fora de uma forma literal nem divisão em classes: ficam com a convenção do repositório e com o diff, e um catálogo de caminhos envelhece e engana o próximo leitor.
- Para cada evento, registre o transporte, a ordenação e a evolução de versão.
- A garantia de entrega vem do transporte escolhido. Não presuma entrega exatamente uma vez, e descreva como duplicações e falhas são tratadas.

## Riscos

- Registre os riscos concretos ainda não tratados pelo contrato ou pelos checks, cada um com mitigação, evidência ou aceitação justificada. Quando uma premissa ou lacuna já descrever o risco, cite-a e acrescente apenas a mitigação necessária.
- Omita a linha cuja única mitigação seja cumprir um requisito, executar um check ou resolver uma lacuna já registrada.
- A tabela sugere técnicas a avaliar, não escolhas obrigatórias.

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

### Forma

- Um check é uma afirmação observável com valor concreto e a prova que a decide:

  ```markdown
  - [ ] **<ID>**: <afirmação> — `<teste ou comando>`
  ```

- A prova é o teste ou o comando cujo exit code decide a afirmação, num trecho de código no fim do item. Sem prova, não há check.
- Um check de decisão técnica começa pelo nome da decisão em vez do ID.
- Derive a afirmação da spec e das decisões. Consulte a implementação para escolher a integração da prova, sem tomar seu resultado atual como resultado esperado.
- Quando o teste ainda não existe, a prova nomeia o teste que a implementação vai criar, pelo comando que o executa. Isso fixa o caminho do teste; os demais caminhos ficam com o diff.

### Escolher a prova

- Identifique framework, estilo e camada nas instruções, na configuração, na CI ou nos testes das áreas atingidas. Leia as fontes necessárias para confirmar os comandos, sem exigir todo esse material para cada mudança.
- Escolha a prova que observa o requisito na camada em que ele é definido.
- Testes de integração, publicação ou mutação entram quando a mudança, a regra local ou o pedido os justifica.
- Quando a mudança não precisar de teste novo, o check nomeia a verificação existente que a cobre.

### Cobertura

- Cada ID de Requirements in Scope aparece em algum check.
- Um requisito sobre um conjunto tem um check por membro nomeado na spec, ou um check que percorre o conjunto inteiro com o tamanho declarado.
- Um requisito que combina dois conjuntos, como operações e estados, tem checks para as combinações que ele afirma.
- Cada decisão irreversível tem um check que prova a forma literal. Quando um check de requisito já exercita a forma literal, nomeie a decisão na afirmação dele em vez de criar outro check.

### Gate

- Reserve o último check para o gate, o comando de verificação do repositório:

  ```markdown
  - [ ] Gate: <o que passa> — `<comando>`
  ```

- O comando do gate vem da configuração do projeto, da CI ou da documentação de build, e é executado na base antes da mudança.
- Sem comando confirmável, registre o comando provável em Assumptions. O gate entra em Checks quando for confirmado.
- Quando for necessário para distinguir regressões, registre em Context o resultado do gate e dos checks existentes na base de comparação.

## Estrutura do documento

- O título é o nome da mudança.
- Use as seções pertinentes, nesta ordem. Checks é a base.
- O modelo `assets/plan.md` começa pelas decisões, provas e pendências. Quando uma seção adicional for necessária, copie apenas o bloco pertinente de [seções opcionais](../assets/plan-sections.md).

| Section | Conteúdo | Forma |
| --- | --- | --- |
| Context | Base de comparação, versão dos artefatos usada, código inspecionado e limitações que afetam a solução | Parágrafos |
| Technical Decisions | Critérios, quando houver comparação, e as decisões | Parágrafo de critérios e tabela Decision, Choice, Rejected alternatives, Cost, Reversible |
| Structure | Caminho, entidades, relações, invariantes, migração e eventos | Lista ou diagrama |
| Risks | Riscos concretos e sua mitigação, evidência ou aceitação | Tabela Risk, Mitigation |
| Assumptions | Inferências e defaults da solução | Lista, como define o fluxo comum |
| Gaps | Informações e decisões ausentes que a solução precisa | Tabela Gap, Affects, Owner |
| Checks | Afirmações com prova | Lista de checkboxes |
| Progress | Fronteira alcançada, decisões do usuário durante a implementação, tentativas descartadas | Lista |
| References | Fontes técnicas consultadas | Lista |

## Exemplo parcial

```markdown
# Repetição de solicitações

| | |
| --- | --- |
| **Requirements in Scope** | `EXM-01`, `EXM-02` |

## Technical Decisions

| Decision | Choice | Rejected alternatives | Cost | Reversible |
| --- | --- | --- | --- | --- |
| Ordenação de solicitações | Sequência por livro, com unicidade em `(book_id, sequence)` | Instante informado pelo cliente: não distingue registros com o mesmo horário | Concorrência sobre a geração da sequência | Não: esquema persistido |

## Checks

- [ ] **EXM-01**: repetir chave e conteúdo retorna o resultado original e mantém uma única solicitação — `dotnet test --filter RequestIdempotencyTests.RepeatReturnsOriginal`
- [ ] **EXM-02**: repetir a chave com outro conteúdo retorna conflito e preserva a primeira solicitação — `dotnet test --filter RequestIdempotencyTests.ConflictKeepsFirst`
- [ ] Ordenação de solicitações: a migração cria a unicidade `(book_id, sequence)` — `dotnet test --filter MigrationTests.SequenceIsUnique`
- [ ] Gate: build e testes passam — `dotnet build && dotnet test`
```
