# Especificação

Defina o comportamento testável de uma capability, das regras de negócio ao resultado técnico que o consumidor observa. A spec é o contrato vivo que o plano e a verificação usam, e registra as regras de negócio que o usuário ou o material de origem decidiram.

## Capability e arquivo

Cada spec descreve uma capability: algo que o sistema faz ou oferece, com um resultado que o consumidor observa, e cujo nome continua válido quando a solução muda. Emissão de fatura é uma capability; reenviar a fatura é uma funcionalidade dela e entra na mesma spec. Uma mudança que não cria resultado novo para o consumidor edita a spec existente em vez de abrir outra.

A spec é dona das regras da sua capability. Nomeie em Affected Capabilities as capabilities cujo resultado a mudança altera, sem redefinir as regras delas. Cite IDs de outra spec só quando consumir a definição, a entrada ou o evento correspondente. Quando a capability afetada não tiver spec e o pedido não incluir o comportamento dela, especifique só o que a sua capability entrega a ela.

## Origem do contrato

| Origem | Evidência e cuidado |
| --- | --- |
| Pedido direto | Registre o comportamento, o consumidor e o resultado informados. Um pedido descrito como tela, microserviço ou CRUD tem por trás um problema do consumidor e uma decisão de negócio: identifique-os, e preserve a interface quando ela for escolha explícita do usuário |
| Documento de produto, ata ou ticket | Pese cada afirmação pela autoridade, porque decisão registrada, observação e sugestão pesam diferente. Cite a origem com seção ou página e sintetize em vez de reformatar |
| Código existente | Descreva o comportamento observado com `arquivo:linha` e as divergências com a intenção documentada. A intenção inferida vai para Assumptions, com a evidência; a justificativa ausente e as intenções concorrentes vão para Gaps. Não reescreva o comportamento para concordar com uma intenção inferida |

Um domínio amplo ou várias iniciativas pedem um recorte com resultado identificável; se a escolha mudar o escopo materialmente, peça a decisão e avance nas partes independentes. Com apenas um nome ou uma ideia genérica, reúna as perguntas indispensáveis sobre problema, consumidor e resultado esperado. Leia a spec existente, os ADRs pertinentes, os contratos e o código atingido antes de perguntar.

Num assunto regulado, distinga o que a norma diz, a interpretação adotada e a regra do sistema: a interpretação do modelo não comprova conformidade.

## Superfícies e dimensões

Percorra as superfícies que a mudança expõe e todas as dimensões do sistema, e registre em Observable Decisions onde cada decisão aterrissou: num requisito, numa garantia que o código já oferece, com a citação, ou numa premissa ou lacuna. Reúna as que não se aplicam numa única linha `n/a`, cada uma com o motivo em poucas palavras; o motivo separa a decisão inaplicável da que ninguém tomou. Uma mudança trivial ou sem superfície exposta registra isso numa linha.

| Superfície | Decisões que ela sempre carrega |
| --- | --- |
| Tela ou visão | Estados vazio, de carregamento, de erro e de não autorizado; ordenação e densidade; o que uma ação destrutiva confirma antes de executar |
| API ou webhook | Formato da resposta, formato do erro e seus códigos, quem pode chamar, versionamento, compatibilidade, comportamento no limite de taxa; ao substituir uma interface, o que deixa de ser atendido, os consumidores afetados, o custo de migração e o prazo de transição decidido |
| Comando ou tarefa agendada | Formato e verbosidade da saída, cada flag e seu default, exit codes, o que registra ao falhar no meio |
| Documento ou texto lido por alguém | Estrutura, profundidade e a ação esperada do leitor |
| Coleção organizada | Critério de agrupamento, nomeação, ordenação, tratamento de duplicatas e a exceção que não se encaixa |

O formato de erro e o estado vazio são as decisões que mais escapam: o primeiro handler define o formato que os outros copiam, e o estado vazio só aparece para conta nova.

As dimensões são validação e limites, falha e falha parcial, idempotência e duplicação, autorização e limite de taxa, concorrência e ordenação, ciclo de vida dos dados, falha de dependência externa, transições de estado, observabilidade e consistência entre capabilities.

A aterrissagem precisa observar a própria dimensão: reaproveitar o requisito de outra linha a deixa descoberta, e nesse caso a resposta é `n/a` com o motivo, uma premissa ou uma lacuna.

Inclua apenas os requisitos justificados pela mudança, sem ampliar o produto preventivamente.

## Glossário e nomes

Fixe conceitos, relações e restrições antes de escolher os nomes. Use os termos da comunidade de especialistas no idioma da spec, com um termo canônico por conceito e os sinônimos no glossário. Quando o código usar outro idioma, registre o identificador equivalente; sem código, o identificador proposto segue a convenção do projeto.

Quando o mesmo termo tiver regras diferentes em outra capability, cada spec define o seu significado. Vocabulário comum, sozinho, não prova que duas capabilities são uma.

## Requisitos

Descreva o resultado que o consumidor observa: estado, mensagem, valor, evento ou limite. Cite um mecanismo só quando ele fizer parte do contrato ou de uma restrição real; o restante pertence ao plano. Não invente HTTP status, prazo ou mecanismo para preencher a forma.

| Descrição de mecanismo | Comportamento a especificar |
| --- | --- |
| Fila de auditoria | Toda mudança registra quem a realizou e quando |
| Modal de confirmação | Excluir um registro ativo exige confirmação explícita |
| Evento em um broker | Outras capabilities recebem a mudança de estado conforme o contrato do evento |

Use EARS para tornar claras as condições de requisitos novos quando o formato ajudar. Preserve uma formulação existente que já seja igualmente verificável. As palavras-chave seguem o idioma da prosa: em inglês, use a coluna Forma; em português, a última coluna, com as palavras-chave em maiúsculas. Uma proibição usa SHALL NOT ou `NÃO DEVE`.

| Padrão | Forma | Adaptação em português |
| --- | --- | --- |
| Geral | The system SHALL `<resultado>` | O sistema `DEVE` produzir o resultado |
| Evento | WHEN `<gatilho>` THEN the system SHALL `<resultado>` | `QUANDO` ocorrer o gatilho, `ENTÃO` o sistema `DEVE` produzir o resultado |
| Estado | WHILE `<estado>` the system SHALL `<resultado>` | `ENQUANTO` o estado estiver ativo, o sistema `DEVE` manter o comportamento |
| Funcionalidade opcional | WHERE `<funcionalidade presente>` the system SHALL `<resultado>` | `CASO` a funcionalidade esteja presente, o sistema `DEVE` cumprir a condição |
| Condição indesejada | IF `<condição>` THEN the system SHALL `<resposta>` | `SE` ocorrer a condição, `ENTÃO` o sistema `DEVE` responder como definido |
| Composto | WHILE `<estado>`, WHEN `<gatilho>` the system SHALL `<resultado>` | `ENQUANTO` o estado estiver ativo, `QUANDO` ocorrer o gatilho, o sistema `DEVE` produzir o resultado |

Um requisito tem ID estável e representa uma unidade verificável. Obrigações que podem falhar independentemente ficam separadas; uma condição conjunta com efeito indivisível permanece junta.

- **Uma execução decide o requisito.** Percentil, média, taxa de erro e disponibilidade são alvos de serviço, que nenhuma execução isolada satisfaz ou reprova. Mantenha o comportamento no requisito e registre o alvo na dimensão de observabilidade.
- **NFR pelo que ele permite verificar.** Um atributo de qualidade com resultado verificável vira requisito; um atributo usado para comparar soluções vira critério das decisões técnicas do plano, com a origem registrada.
- **Conjunto nomeado.** Um requisito que quantifica sobre um conjunto nomeia os membros ou a fonte que os enumera; sem isso, uma prova sobre dois membros satisfaz a frase inteira.
- **Garantia negativa.** Um requisito de que algo não acontece, como uma duplicata ou uma segunda cobrança, cita o mecanismo quando o código já o oferece, mas não aponta para o plano, que envelhece quando outra mudança troca o mecanismo.
- **Opção fora da condição.** Uma opção aplicável só em determinada condição define também o resultado de recebê-la fora dela. Rejeitar e ignorar são escolhas de negócio distintas.

## Eventos de domínio

A spec da capability produtora define cada evento: gatilho, significado do conteúdo, consumidores conhecidos e, quando o consumidor precisar saber, se o evento pode chegar repetido ou fora de ordem. A spec consumidora cita o evento em vez de redefini-lo. Estados, transições, requisitos e eventos concordam entre si.

Um evento sem consumidor identificado permanece candidato; não o apresente como integração decidida.

## Diagramas

Use Mermaid quando estados, decisões ou trocas de mensagens ficarem mais claros num grafo: `stateDiagram-v2` para estados, `flowchart` para decisões e `sequenceDiagram` para interações. Cite os IDs nos rótulos, mantenha junto do diagrama a tabela de estados com a coluna Identifier e evite aliases reservados, como `end` ou `off`.

## Cenários de aceitação

Cada resultado de aceitação deriva de um requisito ou decisão identificável. Um cenário tem nome, entrada, condições e resultado esperado, e cita os requisitos que verifica; “o usuário consegue usar a função” não discrimina um resultado. Casos de aceitação e de rejeição são cenários distintos.

Para cálculos ou ramificações, inclua os valores intermediários e o ramo; os números coincidem com as fórmulas, e uma mudança quantitativa exige recalcular os cenários atingidos. Use Dado/Quando/Então quando a tabela não expressar o cenário; os marcadores seguem o idioma da prosa e, em português, Dado concorda com o sujeito (Dada, Dados ou Dadas).

Se o contrato não determinar o resultado de um caso limite, registre-o em Gaps em vez de escolher um valor por analogia com outro caso.

## Trade-offs

Registre em Trade-offs as decisões de comportamento do usuário ou do material de origem que custam algo, e cite na decisão os IDs afetados. O custo diz o que se perde e para quem. Se ninguém informou o motivo, escreva isso na célula em vez de inferi-lo. Uma escolha sua com custo é premissa, com o custo na consequência; uma escolha técnica fica nas decisões do plano.

## Prefixo e IDs

O título é o nome da capability. Logo abaixo, a tabela de cabeçalho traz Requirement Prefix e, quando houver, Affected Capabilities.

O prefixo abrevia a capability em letras maiúsculas e dígitos, começando por letra, como `INV` para Emissão de fatura. Não abrevie a área a que a capability pertence, porque o prefixo se repetiria na segunda capability dela. Evite nomes genéricos como `REQ`, que não indicam o dono, e não use `FR` nem `NFR`. Escolha um prefixo que nenhuma outra spec use e preserve o existente ao editar; semelhança de letras, por si só, não exige renomeação.

Defina cada requisito num item de lista que começa pelo ID em negrito, na forma `<PREFIX>-nn`, com pelo menos dois dígitos e uma única sequência por spec.

Estados, motivos e outras enumerações que o código ou os contratos referenciam ficam numa tabela com a coluna Identifier ao lado do nome de exibição. O Identifier traz o nome estável do valor, como `UnderReview`, e requisitos, eventos e diagramas o preservam.

Uma refatoração sem mudança observável preserva os requisitos e usa os testes existentes como evidência. Não modifique a spec só para produzir um diff documental.

## Estrutura do documento

Use `#` para o título e `##` para as seções, nesta ordem. Context e Requirements são a base, e as demais seções dependem do conteúdo. Não altere uma spec existente só para introduzir seções. Quando a forma de uma seção não estiver clara, leia o trecho pertinente do [exemplo](spec-example.md).

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
| Observable Decisions | Decisões de cada superfície e dimensão, com a aterrissagem | Tabela Surface or dimension, Landing |
| Trade-offs | Decisões de comportamento que custam algo | Tabela Decision, Cost, Reason |
| Divergences | Na origem código, diferença entre implementação e intenção documentada | Lista |
| References | Fontes externas e normas consultadas, com link, escopo e data | Lista |
