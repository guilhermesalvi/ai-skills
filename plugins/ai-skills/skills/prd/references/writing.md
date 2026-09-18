# Requisitos e seções

Descreva comportamento observável do produto.

## Fatos e incertezas

Uma afirmação factual precisa de origem: decisão do usuário, regra formalizada, observação ou fonte pertinente. Use `[ASSUMPTION]` para inferência ainda não verificada e `[GAP]` para informação ou decisão ausente. Não preencha uma lacuna com especulação sem tag.

Em Open Questions, dê a cada questão um subtítulo e separe decisão ou premissa, origem, impacto, responsável e resolução ou evidência necessária em parágrafos próprios, quando conhecidos. Priorize a premissa cuja falsidade inviabilizaria a proposta: explique a consequência e a forma de verificá-la. Uma premissa aceita para trabalho não se torna fato por ter sido aprovada.

## Capacidade de produto

Na solução, no resumo e nos requisitos, identifique a mudança que o consumidor observa. Uma implementação específica só é citada quando fizer parte do produto solicitado ou de uma restrição real; o restante pertence ao design técnico.

| Descrição de mecanismo | Comportamento a explicitar |
| --- | --- |
| Fila de auditoria | Toda mudança registra quem a realizou e quando |
| Modal de confirmação | Excluir um registro ativo exige confirmação explícita |
| Portal de upload | Enviar documentos e acompanhar o resultado sem depender da disponibilidade do analista |
| Evento em um broker | Outros contextos recebem a mudança de estado conforme o contrato |

## Domínio e fronteiras

Fixe conceitos, relações, atributos e restrições antes de escolher os nomes. Use os termos da comunidade de especialistas no idioma do PRD; quando o código usar outro idioma, registre no glossário o equivalente estabelecido nesse idioma como identificador. Fundamente nomes novos em fontes primárias; sem equivalente estabelecido, use nome descritivo e registre a lacuna.

Mantenha um termo canônico por contexto e registre sinônimos no glossário. Termos iguais com regras e motivos de mudança diferentes exigem análise antes de unificar contextos. Vocabulário sozinho não prova uma fronteira.

O contexto de origem é dono da decisão. Registre o impacto nos outros contextos sem compartilhar implicitamente seus modelos e siga o mapa de contextos do PRD 0000, quando existir. Para capacidades genéricas, avalie reutilização ou contratação quando a decisão estiver em escopo; no core, preserve os diferenciais e dê precisão aos critérios.

Domain Events no PRD produtor define conteúdo, gatilho e consequência de cada evento e nomeia os contextos consumidores. Um evento sem consumidor identificado permanece candidato, condicionado à identificação de quem usará a mudança; não o apresente como integração decidida. Estados, transições, requisitos e eventos devem concordar.

## Uma regra e seus usos

Cada regra tem definição principal no PRD dono. Resumos e diagramas citam o ID e explicam o contexto necessário; a referência não deve obrigar o leitor a adivinhar o comportamento local. Se uma paráfrase contradizer a regra, preserve a divergência como pendência de produto até haver decisão.

Um PRD cita IDs de outro PRD só quando depende deles: a definição, a entrada ou o evento que consome. Não descreva como outro contexto reage ao seu comportamento; nomeie o contexto afetado e deixe as relações entre capabilities na visão geral. Em Regulatory Considerations, cada norma aponta para requisitos do próprio PRD.

Cada requisito representa uma unidade verificável. Separe obrigações que podem falhar independentemente e mantenha juntas as condições cujo efeito é indivisível. Para uma opção aplicável só em determinada condição, defina também o resultado de recebê-la fora dessa condição; rejeitar e ignorar são escolhas de negócio distintas.

## Visão geral

Crie o PRD 0000 quando a pasta tiver mais de um PRD de capability. Ele concentra Purpose, Contexts, Event Catalog, Flows Between Contexts, Terms per Context e Decisions Delegated to ADR, conforme o conteúdo pertinente. A visão geral explica propósito, responsabilidades e interações entre contextos, com apenas o detalhe necessário para entendê-las. Invariantes, cálculos, critérios de sucesso, decisões de produto e suas fontes ficam no PRD da capability responsável, conforme [uma regra e seus usos](#uma-regra-e-seus-usos).

Event Catalog identifica produtores, consumidores, requisitos de recepção e links para os contratos em Domain Events dos PRDs produtores; é o único lugar que liga um evento aos requisitos dos consumidores. O conteúdo e os candidatos seguem [domínio e fronteiras](#domínio-e-fronteiras).

Decisões delegadas a ADR indicam o requisito que precisam satisfazer. Uma decisão arquitetural ainda ausente não se torna regra de produto por aparecer na visão geral.

## Diagramas

Use Mermaid quando estados, decisões ou trocas de mensagens forem mais claros em um grafo: `stateDiagram-v2` para estados, `flowchart` para decisões e `sequenceDiagram` para interações. Cite os IDs pertinentes nos rótulos e mantenha a tabela de estados e identificadores junto do diagrama.

Evite aliases reservados, como `end` ou `off`; nomes completos reduzem ambiguidades. Confira fechamento, tipo e sintaxe. Inspeção textual não comprova renderização: renderize quando a alteração do diagrama justificar ou informe essa limitação.

## Seções

Use `#` para título, `##` para seções e `###` para agrupamentos úteis. Os títulos aparecem na ordem da tabela. Uma seção entra quando há conteúdo pertinente; não preencha com frases vazias nem imponha número de frases ou linhas.

| Seção | Conteúdo e condição de uso |
| --- | --- |
| Executive Summary | Problema, capacidade proposta e resultado ou métrica conhecida |
| Strategic Alignment | Objetivo de negócio a que a proposta responde, quando o material o cita |
| Context and Problem | Situação observada, impacto, evidências e hipóteses |
| Target User / JTBD | Atores e o trabalho ou resultado de que precisam |
| Opportunity / Hypothesis | Hipótese ainda em validação e como validá-la |
| Proposed Solution | Comportamento proposto, limites e relações, referenciando os requisitos |
| Domain Glossary | Termos necessários, ambiguidades e conceitos do contexto dono |
| Functional Requirements | Requisitos com condição, resultado, ID e prioridade |
| Domain Events | Eventos produzidos ou consumidos e requisitos que os governam |
| Non-functional Requirements | Atributos de qualidade, limites e restrições que orientam o design |
| Regulatory Considerations | Norma realmente consultada, interpretação adotada e IDs deste PRD afetados; lacunas identificadas |
| Non-goals | Funcionalidades adjacentes explicitamente excluídas |
| Declared Trade-offs | Decisão, `*Cost:*` concreto e `*Reason:*` que justifica a escolha |
| Success Metrics | Resultado, indicador, unidade, fonte e limite decidido; condições verificáveis do resultado em produto sem operação real; proteção contra degradação quando pertinente |
| Acceptance Criteria | Cenários que discriminam resultados e limites dos requisitos |
| Dependencies and Risks | Dependência ou risco, origem, impacto e tratamento; contextos afetados |
| Open Questions | Decisões e premissas materiais ainda abertas, com impacto e responsável |
| Weakest Point | Decisão frágil, risco, mitigação e condição de reavaliação |
| References | Fontes externas usadas, escopo e datas reais de consulta |

Executive Summary, Context and Problem, Target User / JTBD, Proposed Solution e Functional Requirements formam a base de uma nova capability. Weakest Point, quando existe, só é seguida de References. A visão geral tem estrutura própria. Não altere documentos existentes só para introduzir seções opcionais. Se o pedido exigir outra seção, preserve-a e explique sua finalidade; o formato da skill não anula o pedido.

## Aceitação, pendências e decisões

Um caso de aceitação precisa de nome, entrada, condições e resultado esperado. Para cálculos ou ramificações, prefira tabela com valores intermediários, ramo e alocação ou resultado. Dado/Quando/Então é útil quando uma tabela não expressa o cenário: escreva os marcadores no idioma da prosa, em português flexionando Dado conforme o sujeito (Dada, Dados ou Dadas), e cite os requisitos verificados. "O usuário consegue usar a função" não discrimina um resultado.

Separe condições de entrada das convenções de leitura e precisão dos exemplos. As tabelas numéricas devem coincidir com as fórmulas; alterações quantitativas autorizadas exigem recalcular os exemplos atingidos.

Open Questions segue [fatos e incertezas](#fatos-e-incertezas). Decisões tomadas com custo pertencem a Declared Trade-offs: apresente cada decisão sob um subtítulo `###`, com `*Cost:*` e `*Reason:*` em parágrafos separados. Escolhas técnicas podem pertencer a ADR. Weakest Point discute uma fragilidade material conforme a tabela de seções; não invente risco para preenchê-la.

Em Success Metrics, mantenha Leading, Lagging e Guardrails como grupos distintos, com um item por critério. Métricas e proteções precisam de origem. Em produto sem operação real, como uma plataforma demonstrativa, use condições verificáveis do comportamento em vez de indicadores de uso ou de negócio. Se uma proteção for necessária mas seu limite não estiver definido, registre a lacuna; não crie um indicador ou meta apenas para preencher a seção.
