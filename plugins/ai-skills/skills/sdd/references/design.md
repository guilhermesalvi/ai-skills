# Design da solução

Defina como cumprir a spec, com profundidade proporcional ao risco. O design escolhe estrutura, componentes, contratos e reutilização; uma nova decisão de comportamento volta à spec e, quando for de negócio, ao PRD.

## Contexto pertinente

Leia a spec, os ADRs que restringem a mudança, os tradeoffs e NFRs do PRD e o mapa de contextos quando houver integração. No código, siga do contrato público para as implementações necessárias: módulos, interfaces, domínio, casos de uso e infraestrutura.

Registre o que foi inspecionado e limitações relevantes. Uma regra escrita é convenção; um padrão inferido de poucos exemplos é hipótese. Leia o código que a mudança atinge, não o repositório inteiro.

Para componentes novos, identifique o que será reutilizado e por que outra estrutura é necessária. Problemas adjacentes encontrados são registrados quando afetarem a decisão; não expandem automaticamente o escopo. Nunca exponha segredos ou dados pessoais ao citar evidência.

## Critérios antes das alternativas

Defina os critérios a partir dos requisitos, ADRs, restrições, custo e prazo. Um critério descreve qualidade ou limite, não o mecanismo preferido. Confira se falta algum critério que poderia inverter a escolha antes de comparar soluções.

Compare alternativas reais pelo mesmo escopo e pelos mesmos critérios. Recomende a opção que atende ao contrato com custo e risco justificáveis, explicando o custo aceito. Se não houver alternativa materialmente viável, registre o motivo em vez de inventar opções.

Para cada decisão relevante, confira se atende ao negócio, aos atributos de qualidade e às restrições, e se existe uma solução mais simples ou menos arriscada que também satisfaça o contrato.

## Riscos e técnicas

Registre riscos concretos da mudança e associe cada um a mitigação, evidência ou aceitação justificada. A tabela contém exemplos de técnicas, não escolhas obrigatórias.

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

Para cada componente, descreva responsabilidade, caminho, interfaces com tipos, dependências e reutilização. Contratos consumidos pelas tarefas precisam ser claros antes da implementação.

Eventos definem produtor, consumidores conhecidos, significado do payload, ordenação necessária, garantia de entrega e evolução de versão. A garantia vem do design e do transporte escolhido; não presuma entrega exatamente uma vez. Descreva como duplicações e falhas são tratadas quando possíveis.

Se houver persistência, explicite entidades, relações, invariantes e migração. Para cada cenário de erro da spec em escopo, mostre tratamento e efeito observável; não introduza um novo resultado para facilitar a solução.

## Módulo, publicação e implantação

Distinga módulo de código, pacote versionado e unidade que sobe e desce em conjunto. Avalie primeiro uma mudança no serviço existente, depois um módulo interno e, quando houver necessidade concreta, uma nova unidade implantável.

Uma nova unidade exige justificar a independência necessária, seu dono, operação, contrato e compatibilidade. Necessidades comprovadas de isolamento, escala ou cadência podem pesar na escolha; compare seu custo com opções dentro do serviço existente.

Biblioteca compartilhada precisa de dono, consumidores, estabilidade suficiente e comparação com alternativas existentes. Não extraia regras de negócio para uma biblioteca de plataforma apenas por semelhança de código. Preserve fronteiras públicas e evite ciclos entre módulos.

## Estrutura do documento

Use as seções pertinentes, preservando o formato existente: Design Context, Evaluation Criteria, Risks and Techniques, Approaches, Architecture Overview, Deployment Unit, Components, Domain Events, Data Model, Error Handling, Technical Decisions e Files to Create or Modify.

Technical Decisions registra decisão, escolha, motivo, custo e natureza do contrato: público ou interno. Regras que passam a valer para outras capabilities vão para ADR; decisões locais permanecem no design. Diagramas entram quando tornam as relações mais claras, sem cotas de componentes ou de linhas.

Exemplo didático de decisão:

| Decisão | Escolha | Motivo | Custo | Contrato |
| --- | --- | --- | --- | --- |
| Ordenação de solicitações | Sequência por livro | O requisito hipotético exige ordem total com instantes iguais | Concorrência sobre a geração da sequência | Interno |

Use requisitos e mecanismos reais na entrega; a tabela não adota essa escolha para o projeto.
