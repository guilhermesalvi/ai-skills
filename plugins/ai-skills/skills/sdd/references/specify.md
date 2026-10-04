# Especificação

Defina o comportamento testável de uma capability, das regras de negócio ao resultado técnico que o consumidor observa. A spec é o contrato vivo que o plano e a verificação usam.

Conteúdo: Capability e arquivo · Origem do contrato · Observable Decisions · Glossário e nomes · Requisitos · Prefixo, IDs e identificadores · Eventos de domínio · Diagramas · Cenários de aceitação · Trade-offs · Estrutura do documento

## Capability e arquivo

- Descreva uma capability por spec, conforme o termo do fluxo comum.
- Inclua uma funcionalidade na spec da capability a que pertence. Emissão de fatura é uma capability; reenviar a fatura é uma funcionalidade dela.
- Quando a funcionalidade só acrescentar uma operação ou transição ao ciclo existente, mantenha-a na mesma capability.
- Quando a funcionalidade pertence a uma capability que ainda não tem spec, crie a spec da capability, com o nome dela, e não uma spec da funcionalidade.
- Na primeira spec de uma capability, especifique também o comportamento existente de que a mudança depende, como estados, transições e recusas, a partir do código e com `arquivo:linha`. O resto da capability entra quando outra mudança o atingir. Assim os IDs e o diagrama já nascem na forma que as próximas mudanças vão estender.
- Uma mudança que não cria resultado novo para o consumidor edita a spec existente em vez de abrir outra.
- Mantenha as regras da capability na spec que a define.
- Nomeie em Affected Capabilities as capabilities cujo resultado a mudança altera, sem redefinir as regras delas.
- Uma capability que talvez seja afetada, sem confirmação, vai para Gaps, e não para Affected Capabilities.
- Cite IDs de outra spec só quando consumir a definição, a entrada ou o evento correspondente.
- Quando a capability afetada não tiver spec e o pedido não incluir o comportamento dela, especifique só o que a sua capability entrega a ela.

## Origem do contrato

| Origem | Evidência e cuidado |
| --- | --- |
| Pedido direto | Registre o comportamento, o consumidor e o resultado informados. Um pedido descrito como tela, microserviço ou CRUD tem por trás um problema do consumidor e uma decisão de negócio: identifique-os. Preserve a interface quando ela for escolha explícita do usuário |
| Documento de produto, ata ou ticket | Pese cada afirmação pela autoridade: decisão registrada, observação e sugestão pesam diferente. Cite a origem com seção ou página e sintetize em vez de reformatar |
| Código existente | Descreva o comportamento observado com `arquivo:linha` e as divergências com a intenção documentada. A intenção inferida vai para Assumptions, com a evidência. A justificativa ausente e as intenções concorrentes vão para Gaps. Não reescreva o comportamento para concordar com uma intenção inferida |

- Antes de perguntar, leia a spec existente, os ADRs pertinentes, os contratos e o código atingido.
- Um domínio amplo ou várias iniciativas pedem um recorte com resultado identificável. Um recorte que muda o escopo materialmente é decisão do usuário.
- Com apenas um nome ou uma ideia genérica, reúna as perguntas indispensáveis sobre problema, consumidor e resultado esperado.
- Num assunto regulado, distinga o que a norma diz, a interpretação adotada e a regra do sistema. A interpretação do modelo não comprova conformidade.
- Sem jurisdição conhecida, a norma aplicável é lacuna. Não afirme o conteúdo de uma norma que você não verificou.

## Observable Decisions

### O que a seção registra

Registre em Observable Decisions onde está cada decisão de superfície e de dimensão:

| Registro | Citação em Landing |
| --- | --- |
| Requisito | ID que observa a decisão |
| Garantia existente no código | `arquivo:linha` e o resultado garantido |
| Premissa | Texto em negrito da premissa |
| Lacuna | Texto da coluna Gap |

- Ao mudar a spec, percorra as superfícies que a mudança expõe e todas as dimensões, e atualize as linhas que a mudança atinge.
- Cite em cada linha apenas requisitos que observam aquela dimensão. Reuse um requisito em várias linhas quando ele observar cada uma delas.
- Use apenas IDs ou nomes de premissas e lacunas em Landing quando esses registros já contiverem a decisão. Descreva somente a garantia externa que não está nesses registros, com `arquivo:linha` quando vier do código.
- Vincule a uma premissa ou lacuna a dimensão aplicável que ainda não tiver requisito.
- Reúna as dimensões que não se aplicam numa única linha `n/a`, cada uma como `<Dimension>: <motivo>`. O motivo separa a decisão inaplicável da que ninguém tomou.
- O motivo de um `n/a` não cita requisito: se um requisito observa a dimensão, ela se aplica e tem linha própria.
- Inclua apenas os requisitos justificados pela mudança, sem ampliar o produto preventivamente.

### Dimensões

Os identificadores fazem parte do schema, e o `check_spec.py` exige cada um numa linha própria ou na linha `n/a`.

| Identifier | O que decidir |
| --- | --- |
| Validation and limits | Formatos, tamanhos e faixas aceitos, e o que acontece fora deles |
| Failure and partial failure | O resultado quando a operação falha no meio e o que fica aplicado |
| Idempotency and duplication | O resultado de repetir a mesma operação ou receber a mesma mensagem |
| Authorization | Quem pode executar cada operação e o que recebe quem não pode |
| Rate limiting | O comportamento acima do limite de uso |
| Concurrency and ordering | O resultado de operações simultâneas sobre o mesmo dado e a ordem garantida |
| Data lifecycle | Criação, retenção, exclusão e anonimização dos dados |
| External dependency failure | O resultado quando um serviço externo falha ou demora |
| State transitions | Os estados, as transições permitidas e as recusas |
| Observability | Registros, métricas e alvos de serviço que alguém consulta |
| Cross-capability consistency | O que outras capabilities veem da mudança e quando |

### Superfícies

| Superfície | Decisões que ela sempre carrega |
| --- | --- |
| Tela ou visão | Estados vazio, de carregamento, de erro e de não autorizado; ordenação e densidade; o que uma ação destrutiva confirma antes de executar |
| API ou webhook | Formato da resposta, formato do erro e seus códigos, quem pode chamar, versionamento, compatibilidade, comportamento no limite de taxa. Ao substituir uma interface: o que deixa de ser atendido, os consumidores afetados, o custo de migração e o prazo de transição decidido |
| Biblioteca ou módulo chamado no mesmo processo | Operação pública e suas entradas, com a forma literal da assinatura no plano; erros e como o chamador os distingue; compatibilidade com chamadores existentes; o que o módulo exige do chamador, como identidade autenticada ou chamadas em sequência |
| Comando ou tarefa agendada | Formato e verbosidade da saída, cada flag e seu default, exit codes, o que registra ao falhar no meio |
| Documento ou texto lido por alguém | Estrutura, profundidade e a ação esperada do leitor |
| Coleção organizada | Critério de agrupamento, nomeação, ordenação, tratamento de duplicatas e a exceção que não se encaixa |

O formato de erro e o estado vazio são as decisões que mais escapam: o primeiro handler define o formato que os outros copiam, e o estado vazio só aparece para conta nova.

## Glossário e nomes

- Fixe conceitos, relações e restrições antes de escolher os nomes.
- Use os termos da comunidade de especialistas no idioma da spec, com um termo canônico por conceito e os sinônimos no glossário.
- Quando o código usar outro idioma, registre o identificador equivalente. Sem código, o identificador proposto segue a convenção do projeto.
- Quando o mesmo termo tiver regras diferentes em outra capability, cada spec define o seu significado. Vocabulário comum, sozinho, não prova que duas capabilities são uma.

## Requisitos

### Conteúdo

- Descreva o resultado que o consumidor observa: estado, mensagem, valor, evento ou limite.
- Cite um mecanismo só quando ele fizer parte do contrato ou de uma restrição real. O restante pertence ao plano.
- Não invente HTTP status, prazo ou mecanismo para preencher a forma.

| Descrição de mecanismo | Comportamento a especificar |
| --- | --- |
| Fila de auditoria | Toda mudança registra quem a realizou e quando |
| Modal de confirmação | Excluir um registro ativo exige confirmação explícita |
| Evento em um broker | Outras capabilities recebem a mudança de estado conforme o contrato do evento |

### Formato

- Defina cada requisito num item de lista na forma `- **<PREFIX>-nn** — <requisito>`, com pelo menos dois dígitos e uma única sequência por spec.
- Cada requisito tem ID estável e representa uma unidade verificável.
- Obrigações que podem falhar independentemente ficam em requisitos separados. Uma condição conjunta com efeito indivisível fica num requisito só.

### EARS

- Use EARS para deixar claras as condições de requisitos novos quando o formato ajudar.
- Preserve uma formulação existente que já seja igualmente verificável.
- As palavras-chave seguem o idioma da prosa: em inglês, use a coluna Forma; em português, a última coluna. Escreva-as em maiúsculas, sem formatação de código.
- Use SHALL NOT ou NÃO DEVE para proibições.

| Padrão | Forma | Adaptação em português |
| --- | --- | --- |
| Geral | The system SHALL `<resultado>` | O sistema DEVE produzir o resultado |
| Evento | WHEN `<gatilho>` THEN the system SHALL `<resultado>` | QUANDO ocorrer o gatilho, ENTÃO o sistema DEVE produzir o resultado |
| Estado | WHILE `<estado>` the system SHALL `<resultado>` | ENQUANTO o estado estiver ativo, o sistema DEVE manter o comportamento |
| Funcionalidade opcional | WHERE `<funcionalidade presente>` the system SHALL `<resultado>` | CASO a funcionalidade esteja presente, o sistema DEVE cumprir a condição |
| Condição indesejada | IF `<condição>` THEN the system SHALL `<resposta>` | SE ocorrer a condição, ENTÃO o sistema DEVE responder como definido |
| Composto | WHILE `<estado>`, WHEN `<gatilho>` the system SHALL `<resultado>` | ENQUANTO o estado estiver ativo, QUANDO ocorrer o gatilho, o sistema DEVE produzir o resultado |

### Verificabilidade

- **Uma execução decide o requisito.** Percentil, média, taxa de erro e disponibilidade são alvos de serviço, que nenhuma execução isolada satisfaz ou reprova. Mantenha o comportamento no requisito e registre o alvo na dimensão Observability.
- **NFR pelo que ele permite verificar.** Um atributo de qualidade com resultado verificável vira requisito. Um atributo usado para comparar soluções vira critério das decisões técnicas do plano, com a origem registrada.
- **Conjunto nomeado.** Um requisito que quantifica sobre um conjunto nomeia os membros ou a fonte que os enumera. Sem isso, uma prova sobre dois membros satisfaz a frase inteira.
- **Garantia negativa.** Para exigir que algo não aconteça, como uma segunda cobrança, cite no requisito o mecanismo que o código já oferece, com `arquivo:linha`. Não aponte para o plano, que envelhece quando outra mudança troca o mecanismo.
- **Garantia negativa nova.** Quando o mecanismo ainda não existe no código, o requisito descreve só o resultado, e o plano registra o mecanismo que o sustenta.
- **Opção fora da condição.** Uma opção aplicável só em determinada condição define também o resultado de recebê-la fora dela. Rejeitar e ignorar são escolhas de negócio distintas.

## Prefixo, IDs e identificadores

- O título é o nome da capability. Logo abaixo, a tabela de cabeçalho do modelo traz Requirement Prefix e, quando houver, Affected Capabilities.
- O prefixo abrevia a capability em letras maiúsculas e dígitos, começando por letra, como `INV` para Emissão de fatura.
- Não abrevie a área a que a capability pertence, porque o prefixo se repetiria na segunda capability dela.
- Evite nomes genéricos como `REQ`, que não indicam o dono, e não use `FR` nem `NFR`.
- Escolha um prefixo que nenhuma outra spec use, e preserve o existente ao editar. Semelhança de letras, por si só, não exige renomeação.
- Estados, motivos e outras enumerações que o código ou os contratos referenciam ficam numa tabela com a coluna Identifier ao lado do nome de exibição.
- O Identifier traz o nome estável do valor, como `UnderReview`, e requisitos, eventos e diagramas o preservam.
- Quando o valor tem um nome no código e outra forma serializada, o Identifier traz a forma que o consumidor observa: o nome do membro para quem chama o código no mesmo processo; o valor serializado para quem o recebe por API, evento ou armazenamento.
- Uma refatoração sem mudança observável preserva os requisitos e usa os testes existentes como evidência. Não modifique a spec só para produzir um diff documental.

## Eventos de domínio

- A spec da capability produtora define cada evento: gatilho, significado do conteúdo, consumidores conhecidos e, quando o consumidor precisar saber, se o evento pode chegar repetido ou fora de ordem.
- A spec consumidora cita o evento em vez de redefini-lo.
- Estados, transições, requisitos e eventos concordam entre si.
- Um evento sem consumidor identificado não entra em Domain Events. Registre-o em Gaps, com o consumidor como a informação que falta.

## Diagramas

- Use Mermaid quando estados, decisões ou trocas de mensagens ficarem mais claros num grafo: `stateDiagram-v2` para estados, `flowchart` para decisões e `sequenceDiagram` para interações.
- Cite os IDs nos rótulos das transições e mensagens.
- Mantenha junto do diagrama a tabela de estados com a coluna Identifier.
- Evite aliases reservados, como `end` ou `off`.

## Cenários de aceitação

- Inclua Acceptance Scenarios quando um cálculo, ramificação ou combinação de condições precisar de um exemplo que o requisito sozinho não esclarece. Derive cada resultado de um requisito ou de uma decisão identificável.
- Exclua o cenário cujas condições e resultado apenas repetem o requisito. Mantenha a prova correspondente nos Checks do plano.
- Um cenário tem nome, entrada, condições e resultado esperado, e cita os requisitos que verifica. "O usuário consegue usar a função" não discrimina um resultado.
- Casos de aceitação e de rejeição são cenários distintos.
- Para cálculos ou ramificações, inclua os valores intermediários e o ramo. Os números coincidem com as fórmulas, e uma mudança quantitativa exige recalcular os cenários atingidos.
- Use Dado/Quando/Então quando a tabela não expressar o cenário. Os marcadores seguem o idioma da prosa e, em português, Dado concorda com o sujeito (Dada, Dados ou Dadas).
- Se o contrato não determinar o resultado de um caso limite, registre-o em Gaps em vez de escolher um valor por analogia com outro caso.

## Trade-offs

- Registre em Trade-offs as decisões de comportamento do usuário ou do material de origem que custam algo, e cite na decisão os IDs afetados.
- O custo diz o que se perde e para quem.
- Se ninguém informou o motivo, escreva isso na célula em vez de inferi-lo.
- Uma escolha sua com custo é premissa, com o custo descrito em `Choice:`. Uma escolha técnica fica nas decisões do plano.

## Estrutura do documento

- Use `#` para o título e `##` para as seções, nesta ordem.
- Context, Requirements e Observable Decisions são a base. As demais seções dependem do conteúdo.
- O modelo `assets/spec.md` começa pelo contrato e pelas pendências. Quando uma seção adicional for necessária, copie apenas o bloco pertinente de [seções opcionais](../assets/spec-sections.md).
- Não altere uma spec existente só para introduzir seções.

| Section | Conteúdo | Forma |
| --- | --- | --- |
| Context | Problema, consumidor e o trabalho que ele precisa fazer, origem do contrato e código pertinente | Parágrafos |
| Scope | O que entra e as exclusões que um leitor esperaria ver dentro | Parágrafo ou lista |
| Assumptions | Inferências e defaults de comportamento | Lista, como define o fluxo comum |
| Gaps | Informações e decisões ausentes | Tabela Gap, Affects, Owner |
| Glossary | Termos canônicos, sinônimos e identificadores no idioma do código | Tabela Term, Identifier, Definition |
| Requirements | IDs e comportamento observável, com os diagramas pertinentes | Lista de requisitos; tabela State, Identifier, Meaning para estados |
| Domain Events | Gatilho, significado, consumidores e o que eles podem assumir | Tabela Event, Trigger, Content, Consumers |
| Acceptance Scenarios | Nome, entrada, condições, resultado e requisitos verificados | Tabela Scenario, Input, Condition, Requirements, Result |
| Observable Decisions | Onde está cada decisão de superfície e de dimensão | Tabela Surface or dimension, Landing |
| Trade-offs | Decisões de comportamento que custam algo | Tabela Decision, Cost, Reason |
| Divergences | Na origem código, diferença entre implementação e intenção documentada | Lista |
| References | Fontes externas e normas consultadas | Lista |
