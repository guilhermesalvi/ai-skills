# Plano e tarefas

Produza um plano que outro executor consiga seguir sem adivinhar comportamento, decisões ou dependências. O plano decide como cumprir a spec, com profundidade proporcional ao risco, e divide o trabalho em tarefas; cada tarefa entrega uma mudança coesa, com implementação, integração e verificação pertinentes. Uma nova decisão de comportamento volta à spec.

## Contexto pertinente

Leia a spec, os ADRs que restringem a mudança e o código que ela atinge, não o repositório inteiro: siga do contrato público para as implementações necessárias. Registre o que foi inspecionado e as limitações relevantes. Nunca exponha segredos ou dados pessoais ao citar evidência.

Distinga o peso de cada fonte: uma regra escrita é convenção, enquanto um padrão inferido de poucos exemplos é hipótese. Para componentes novos, identifique o que será reutilizado e por que outra estrutura é necessária.

Problemas adjacentes entram no plano quando afetarem uma decisão; eles não expandem o escopo.

## Conhecer a verificação do projeto

Leia as instruções das áreas atingidas, a documentação de build e testes, a configuração dos projetos e a CI.

Inspecione os testes pertinentes para entender framework, estilo e camada. Não imponha uma amostra fixa nem copie todos os níveis de teste para qualquer tarefa.

Registre no plano o estado inicial dos checks quando ele for necessário para distinguir regressões. Uma contagem histórica não substitui os resultados dos testes.

Escolha a verificação que observa o requisito. Testes de domínio, integração, publicação ou mutação entram quando a mudança, a regra local ou o pedido os justifica. A ausência de uma ferramenta é uma limitação a resolver ou reportar, nunca motivo para declarar sucesso fictício.

## Decisões técnicas

Registre as escolhas que outro executor não deduziria da spec e do código.

Defina os critérios antes de comparar soluções, a partir dos requisitos, ADRs, restrições, custo e prazo. Um critério descreve qualidade ou limite, não o mecanismo preferido; confira se falta algum que poderia inverter a escolha. Compare alternativas reais pelo mesmo escopo e pelos mesmos critérios, e escolha a que atende ao contrato com custo e risco justificáveis. Se não houver alternativa materialmente viável, registre o motivo em vez de inventar opções.

Rejeite uma alternativa pela propriedade que a desqualifica, como “não expressa o próximo estado”, e não por preferência, como “mais limpo”, que ninguém consegue contestar. Confira se uma solução mais simples ou menos arriscada também satisfaz o contrato.

Use a arquitetura do projeto quando ela atende ao problema. Módulo de código, pacote versionado e unidade que sobe e desce em conjunto são decisões distintas: avalie primeiro uma mudança no serviço existente, depois um módulo interno e, só com necessidade concreta de isolamento, escala ou cadência, uma nova unidade implantável, com dono, operação, contrato e compatibilidade. Uma biblioteca compartilhada precisa de dono, consumidores e estabilidade suficiente; não extraia regras de negócio para ela apenas por semelhança de código.

Uma regra que passa a valer para outras capabilities, como um novo estilo arquitetural, vai para [ADR](adr.md), dentro da autorização existente; decisões locais ficam no plano.

Marque como irreversível, com o motivo, a decisão cujo desfazer custa mais que uma refatoração: esquema persistido, contrato que outro consome, dependência nova, migração sobre dados existentes ou precedente que o repositório ainda não tem. Registre nela a forma literal que o próximo leitor vai copiar, como a definição do índice, o valor do enum ou a versão do pacote, ou cite a seção Estrutura que a mostra. Escopo adiado e regra sem mecanismo se desfazem sem esse custo e não entram.

Registre as decisões numa tabela. Quando uma escolha exigir comparação, os critérios e sua origem vêm num parágrafo antes da tabela.

| Decisão | Escolha | Alternativas rejeitadas | Custo | Reversível |
| --- | --- | --- | --- | --- |
| Ordenação de solicitações | Sequência por livro, com unicidade em `(book_id, sequence)` | Instante informado pelo cliente: não distingue registros com o mesmo horário | Concorrência sobre a geração da sequência | Não: esquema persistido |

## Estrutura e riscos

Descreva os componentes novos ou alterados com responsabilidade, interfaces com tipos e o que reutilizam e, se houver persistência, entidades, relações, invariantes e migração. Os contratos que as tarefas consomem precisam estar claros antes da implementação. Pasta, nome de arquivo e divisão em classes ficam com a convenção do repositório e com o diff: um catálogo de caminhos envelhece e engana o próximo leitor.

Para cada evento, registre o transporte, a ordenação e a evolução de versão. A garantia de entrega vem do transporte escolhido: não presuma entrega exatamente uma vez, e descreva como duplicações e falhas são tratadas.

O tratamento de cada cenário de erro da spec fica na tarefa que o implementa, com o requisito que define o efeito observável. Não introduza um novo resultado para facilitar a solução.

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

## Unidade de trabalho

Uma tarefa tem um resultado integrável: por exemplo, operação com validação, registro no módulo e testes correspondentes. Divida resultados independentes. Se os testes só puderem executar depois de uma dependência, ajuste o agrupamento para entregar algo verificável.

O título da tarefa diz o resultado, e os campos completam o que ele não diz:

| Campo | Conteúdo |
| --- | --- |
| Onde | Caminhos já determinados, distinguindo criação e alteração; omita o campo quando a colocação ficar com o executor |
| Depende de | IDs das dependências ou `nenhuma` |
| Interfaces | Contratos consumidos e produzidos, com tipos e erros pertinentes |
| Pronto quando | Um critério observável e binário por resultado, com o ID do requisito e o teste que o decide, e por último o comando de gate |

O texto de Interfaces precisa ser suficiente para entender a tarefa; a spec e a seção Estrutura permitem conferir o contrato completo. Não invente uma interface ausente nem use “similar à tarefa anterior” como especificação.

Pronto quando aponta o teste que decide cada requisito, não a suíte verde. Um requisito sobre um conjunto tem um caso por membro nomeado na spec, ou um caso que percorre o conjunto inteiro com o tamanho declarado. Quando a tarefa não precisar de teste novo, o critério nomeia a verificação existente que a cobre.

O comando de gate está confirmado na configuração real do projeto ou nomeia um check de Comandos de gate.

## Ordem e rastreabilidade

Ordene por dependência, sem ciclos nem referência a uma tarefa inexistente. Agrupe por coesão: fases fixas de fundação, domínio e adapters não são obrigatórias.

Cada requisito em escopo aparece no Pronto quando de alguma tarefa. Esses IDs já formam a rastreabilidade: não os repita numa tabela à parte. Um requisito que nenhuma tarefa verifica está fora do escopo declarado ou é lacuna do plano, e precisa de resposta antes da execução. Não atribua a uma tarefa um requisito que ela não verifica.

A última tarefa de uma fase não exige repetir toda a suíte quando já existe evidência válida para o mesmo estado; uma mudança posterior ou uma falha justifica repetir os checks afetados.

## Estrutura do documento

Use as seções pertinentes, nesta ordem; Comandos de gate e Tarefas são a base. Diagramas entram quando tornam as relações mais claras.

| Seção | Conteúdo |
| --- | --- |
| Contexto | Base de comparação, código inspecionado e limitações que afetam a solução |
| Decisões técnicas | Critérios, quando houver comparação, e a tabela de decisões |
| Estrutura | Componentes, interfaces, eventos, modelo de dados e migração |
| Riscos | Riscos concretos e sua mitigação, evidência ou aceitação |
| Premissas | Inferências e escolhas provisórias da solução |
| Lacunas | Informações e decisões ausentes que a solução precisa |
| Comandos de gate | Checks pertinentes, como `quick`, `full` e `build`, se esses nomes ajudarem |
| Tarefas | Tarefas com os campos da unidade de trabalho |

## Exemplo parcial

```markdown
### T1: Criar solicitações de forma idempotente

- **Onde:** criar `src/Example/Requests/RequestService.cs` e os testes correspondentes
- **Depende de:** nenhuma
- **Interfaces:** consome `CreateRequest` e armazenamento por chave; produz `CreateResult` com solicitação ou conflito
- **Pronto quando:**
  - [ ] EXM-01: repetir chave e conteúdo retorna o resultado original sem duplicar; teste de repetição equivalente
  - [ ] EXM-02: repetir a chave com outro conteúdo informa conflito e preserva a primeira solicitação; teste de conflito
  - [ ] `quick` passa
```
