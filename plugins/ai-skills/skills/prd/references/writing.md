# Requisitos e seções

Descreva comportamento observável do produto.

## Fatos e incertezas

Toda afirmação factual precisa de origem: decisão do usuário, regra formalizada, observação ou fonte pertinente. Sem origem, marque o texto:

- `[PREMISSA]` para inferência ainda não verificada, com a origem ou evidência que a motivou.
- `[LACUNA]` para informação ou decisão ausente.

Não preencha uma lacuna com especulação sem tag. Usuário, métrica, limite ou regra ausente continua lacuna: não invente um valor para tornar a frase aparentemente verificável.

Quando regras, fontes ou paráfrases se contradisserem, ou quando uma correção depender de decisão de negócio, registre um `[LACUNA]` com os IDs afetados e conclua o restante. Não escolha uma das versões em silêncio.

## Capacidade de produto

Na solução, no resumo e nos requisitos, identifique a mudança que o consumidor observa. Cite uma implementação específica apenas quando ela fizer parte do produto solicitado ou de uma restrição real; o restante pertence ao design técnico.

| Descrição de mecanismo | Comportamento a explicitar |
| --- | --- |
| Fila de auditoria | Toda mudança registra quem a realizou e quando |
| Modal de confirmação | Excluir um registro ativo exige confirmação explícita |
| Portal de upload | Enviar documentos e acompanhar o resultado sem depender da disponibilidade do analista |
| Evento em um broker | Outros contextos recebem a mudança de estado conforme o contrato |

## Domínio e fronteiras

### Conceitos antes de nomes

Fixe conceitos, relações, atributos e restrições antes de escolher os nomes.

Use os termos da comunidade de especialistas no idioma do PRD. Quando o código usar outro idioma, registre no glossário o equivalente estabelecido nesse idioma como identificador. Fundamente nomes novos em fontes primárias; sem equivalente estabelecido, use um nome descritivo e registre a lacuna.

Mantenha um termo canônico por contexto e registre os sinônimos no glossário. Termos iguais com regras e motivos de mudança diferentes exigem análise antes de unificar contextos: vocabulário sozinho não prova uma fronteira.

### Responsabilidade entre contextos

O contexto de origem é dono da decisão. Registre o impacto nos outros contextos sem compartilhar implicitamente seus modelos, e siga o mapa de contextos do PRD 0000 quando ele existir.

Para capacidades genéricas, avalie reutilização ou contratação quando a decisão estiver em escopo. No core, preserve os diferenciais e dê precisão aos critérios.

### Eventos

A seção Eventos de domínio, no PRD produtor, define conteúdo, gatilho e consequência de cada evento, e nomeia os contextos consumidores. Estados, transições, requisitos e eventos devem concordar entre si.

Um evento sem consumidor identificado permanece candidato, condicionado à identificação de quem usará a mudança; não o apresente como integração decidida.

## Uma regra e seus usos

Cada regra tem definição principal no PRD dono dela. Resumos e diagramas citam o ID e explicam o contexto necessário: a referência não pode obrigar o leitor a adivinhar o comportamento local.

Um PRD cita IDs de outro PRD só quando depende deles, isto é, quando consome a definição, a entrada ou o evento. Não descreva como outro contexto reage ao seu comportamento: nomeie o contexto afetado e deixe as relações entre capabilities na visão geral. Em Considerações regulatórias, cada norma aponta para requisitos do próprio PRD.

Cada requisito representa uma unidade verificável. Separe obrigações que podem falhar independentemente e mantenha juntas as condições cujo efeito é indivisível.

Para uma opção aplicável apenas em determinada condição, defina também o resultado de recebê-la fora dessa condição. Rejeitar e ignorar são escolhas de negócio distintas.

## Diagramas

Use Mermaid quando estados, decisões ou trocas de mensagens ficarem mais claros em um grafo: `stateDiagram-v2` para estados, `flowchart` para decisões e `sequenceDiagram` para interações.

Cite os IDs pertinentes nos rótulos e mantenha a tabela de estados e identificadores junto do diagrama. Evite aliases reservados, como `end` ou `off`, e confira fechamento, tipo e sintaxe.

Inspeção textual não comprova renderização. Renderize quando a alteração do diagrama justificar, ou informe essa limitação.

## Seções

Use `#` para o título, `##` para as seções e `###` para agrupamentos úteis. Os títulos seguem a ordem da tabela, e só Referências pode vir depois de Ponto mais frágil.

As seções marcadas como base são obrigatórias numa nova capability. As demais entram quando há conteúdo pertinente, sem frases vazias. Não altere documentos existentes só para introduzir seções opcionais. Se o pedido exigir outra seção, preserve-a e explique sua finalidade.

| Seção | Base | Conteúdo |
| --- | --- | --- |
| Resumo executivo | Sim | Problema, capacidade proposta e resultado ou métrica conhecida |
| Alinhamento estratégico | | Objetivo de negócio que o material cita e a que a proposta responde |
| Contexto e problema | Sim | Situação observada, impacto, evidências e hipóteses |
| Usuário-alvo / JTBD | Sim | Atores e o trabalho ou resultado de que precisam |
| Oportunidade / hipótese | | Hipótese ainda em validação e como validá-la |
| Solução proposta | Sim | Comportamento proposto, limites e relações, referenciando os requisitos |
| Glossário do domínio | | Termos necessários, ambiguidades e conceitos do contexto dono |
| Requisitos funcionais | Sim | Requisitos com condição, resultado, ID e prioridade |
| Eventos de domínio | | Eventos produzidos ou consumidos e requisitos que os governam |
| Requisitos não funcionais | | Atributos de qualidade, limites e restrições que orientam o design, com ID e prioridade |
| Considerações regulatórias | | Norma realmente consultada, interpretação adotada, IDs deste PRD afetados e lacunas |
| Fora do escopo | | Funcionalidades adjacentes explicitamente excluídas |
| Trade-offs declarados | | Decisões tomadas que custam algo |
| Métricas de sucesso | | Indicadores de resultado e proteções contra degradação |
| Critérios de aceitação | | Cenários que discriminam resultados e limites dos requisitos |
| Dependências e riscos | | Dependência ou risco, origem, impacto e tratamento; contextos afetados |
| Questões em aberto | | Decisões e premissas materiais ainda abertas |
| Ponto mais frágil | | Decisão frágil, risco, mitigação e condição de reavaliação |
| Referências | | Fontes externas usadas, escopo e datas reais de consulta |

### Trade-offs declarados

Apresente cada decisão sob um subtítulo `###`, com `*Custo:*` concreto e `*Motivo:*` em parágrafos separados. Escolhas técnicas podem pertencer a um ADR.

### Métricas de sucesso

Mantenha Leading, Lagging e Guardrails como grupos distintos, com um item por critério e a origem de cada métrica ou proteção. Registre resultado, indicador, unidade, fonte e limite decidido.

Em produto sem operação real, como uma plataforma demonstrativa, use condições verificáveis do comportamento em vez de indicadores de uso ou de negócio.

### Critérios de aceitação

Um caso de aceitação precisa de nome, entrada, condições e resultado esperado. “O usuário consegue usar a função” não discrimina um resultado.

Para cálculos ou ramificações, prefira uma tabela com valores intermediários, ramo e alocação ou resultado. As tabelas numéricas devem coincidir com as fórmulas, e uma alteração quantitativa autorizada exige recalcular os exemplos atingidos. Separe as condições de entrada das convenções de leitura e precisão dos exemplos.

Use Dado/Quando/Então quando a tabela não expressar o cenário, e cite os requisitos verificados. Os marcadores seguem o idioma da prosa; em português, flexione Dado conforme o sujeito (Dada, Dados ou Dadas).

### Questões em aberto

Dê um subtítulo a cada questão e separe em parágrafos próprios, quando conhecidos, a decisão ou premissa, a origem, o impacto, o responsável e a resolução ou evidência necessária.

Priorize a premissa cuja falsidade inviabilizaria a proposta: explique a consequência e a forma de verificá-la. Uma premissa aceita para o trabalho continuar não vira fato por ter sido aprovada.
