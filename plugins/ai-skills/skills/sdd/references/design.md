# Design da solução

Defina como cumprir a spec, com profundidade proporcional ao risco. O design escolhe estrutura, componentes, contratos e reutilização. Uma nova decisão de comportamento volta à spec e, quando for de negócio, ao PRD.

## Contexto pertinente

Leia a spec, os ADRs que restringem a mudança, os trade-offs e NFRs do PRD e o mapa de contextos quando houver integração. No código, siga do contrato público para as implementações necessárias: módulos, interfaces, domínio, casos de uso e infraestrutura.

Leia o código que a mudança atinge, não o repositório inteiro. Registre o que foi inspecionado e as limitações relevantes. Nunca exponha segredos ou dados pessoais ao citar evidência.

Distinga o peso de cada fonte: uma regra escrita é convenção, enquanto um padrão inferido de poucos exemplos é hipótese.

Para componentes novos, identifique o que será reutilizado e por que outra estrutura é necessária.

Problemas adjacentes encontrados entram no design quando afetarem a decisão; eles não expandem automaticamente o escopo.

## Critérios antes das alternativas

Defina os critérios a partir dos requisitos, ADRs, restrições, custo e prazo. Um critério descreve qualidade ou limite, não o mecanismo preferido. Antes de comparar soluções, confira se falta algum critério que poderia inverter a escolha.

Compare alternativas reais pelo mesmo escopo e pelos mesmos critérios. Recomende a opção que atende ao contrato com custo e risco justificáveis, explicando o custo aceito. Se não houver alternativa materialmente viável, registre o motivo em vez de inventar opções.

Rejeite uma alternativa pela propriedade que a desqualifica, como “não expressa o próximo estado”, e não por preferência, como “mais limpo”, que ninguém consegue contestar.

Confira cada decisão relevante contra o negócio, os atributos de qualidade e as restrições, e verifique se existe uma solução mais simples ou menos arriscada que também satisfaça o contrato.

## Riscos e técnicas

Registre riscos concretos da mudança e associe cada um a mitigação, evidência ou aceitação justificada. A tabela sugere técnicas a avaliar, não escolhas obrigatórias.

| Risco | Técnicas a avaliar conforme o contrato |
| --- | --- |
| Evento perdido ou estado inconsistente | Contrato de entrega, consistência e publicação transacional ou equivalente |
| Concorrência, repetição ou reordenação | Chave de idempotência, controle de versão, restrição de unicidade, transições explícitas |
| Integração instável | Isolamento do contrato, timeout, política de repetição e tratamento de indisponibilidade |
| Cálculo financeiro | Precisão, arredondamento e regras isoladas com cenários numéricos |
| Migração ou incompatibilidade | Sequência de transição, compatibilidade e recuperação |
| Desempenho | Orçamento medido, paginação e índices pertinentes |
| Dados regulados ou autorização | Fronteira de acesso, retenção, auditoria e redução de exposição |

Use a arquitetura do projeto quando ela atende ao problema. Introduzir um novo estilo que afete outras capabilities pede uma decisão explícita registrada em [ADR](adr.md), dentro da autorização existente.

## Componentes, contratos e dados

Para cada componente, descreva responsabilidade, interfaces com tipos e o que reutiliza. Os contratos consumidos pelas tarefas precisam estar claros antes da implementação.

Pasta, nome de arquivo e divisão em classes ficam com a convenção do repositório e com o diff. Um catálogo de caminhos e dependências por componente envelhece e engana o próximo leitor.

Os eventos definem produtor, consumidores conhecidos, significado do payload, ordenação necessária, garantia de entrega e evolução de versão. A garantia vem do design e do transporte escolhido: não presuma entrega exatamente uma vez. Descreva como duplicações e falhas são tratadas quando forem possíveis.

Se houver persistência, explicite entidades, relações, invariantes e migração.

Para cada cenário de erro da spec em escopo, mostre tratamento e efeito observável. Não introduza um novo resultado para facilitar a solução.

Antes de apresentar o design, confira que cada requisito em escopo aterrissa num componente, contrato, fluxo ou estrutura de dados. O que não aterrissa está fora do escopo declarado ou é lacuna da solução, e precisa de resposta antes da decomposição.

## Módulo, publicação e implantação

Módulo de código, pacote versionado e unidade que sobe e desce em conjunto são decisões distintas; não trate uma como consequência da outra.

Avalie as opções nesta ordem: primeiro uma mudança no serviço existente, depois um módulo interno e, quando houver necessidade concreta, uma nova unidade implantável.

Uma nova unidade exige justificar a independência necessária, seu dono, operação, contrato e compatibilidade. Necessidades comprovadas de isolamento, escala ou cadência podem pesar na escolha; compare seu custo com as opções dentro do serviço existente.

Uma biblioteca compartilhada precisa de dono, consumidores, estabilidade suficiente e comparação com alternativas existentes. Não extraia regras de negócio para uma biblioteca de plataforma apenas por semelhança de código. Preserve fronteiras públicas e evite ciclos entre módulos.

## Estrutura do documento

Use as seções pertinentes, nesta ordem. Diagramas entram quando tornam as relações mais claras.

| Seção | Conteúdo |
| --- | --- |
| Design Context | Fontes lidas, código inspecionado e limitações |
| Evaluation Criteria | Critérios e sua origem |
| Risks and Techniques | Riscos concretos e sua mitigação, evidência ou aceitação |
| Approaches | Alternativas comparadas pelos mesmos critérios e recomendação |
| Architecture Overview | Estrutura da solução e relações entre as partes |
| Deployment Unit | Serviço existente, módulo interno ou nova unidade, com justificativa |
| Components | Responsabilidade, interfaces e reutilização |
| Domain Events | Contrato de cada evento produzido ou consumido |
| Data Model | Entidades, relações, invariantes e migração |
| Error Handling | Tratamento e efeito observável de cada cenário de erro da spec |
| Technical Decisions | Decisão, escolha com sua forma literal, alternativa rejeitada, custo aceito, natureza do contrato, público ou interno, e reversibilidade |
| Files to Create or Modify | Caminhos já determinados, distinguindo criação e alteração |

Regras que passam a valer para outras capabilities vão para ADR; decisões locais permanecem em Technical Decisions.

Marque como irreversível a decisão cujo desfazer custa mais que uma refatoração: esquema persistido, contrato que outro consome, dependência nova, migração sobre dados existentes ou precedente que o repositório ainda não tem. Registre nela a forma literal que o próximo leitor vai copiar, como a definição do índice, o valor do enum ou a versão do pacote. Escopo adiado e regra sem mecanismo se desfazem sem esse custo e não entram.

Exemplo de linha de Technical Decisions:

| Decisão | Escolha e forma literal | Alternativa rejeitada | Custo | Contrato | Reversível |
| --- | --- | --- | --- | --- | --- |
| Ordenação de solicitações | Sequência por livro, com unicidade em `(book_id, sequence)` | Instante informado pelo cliente: não distingue registros com o mesmo horário | Concorrência sobre a geração da sequência | Interno | Não |
