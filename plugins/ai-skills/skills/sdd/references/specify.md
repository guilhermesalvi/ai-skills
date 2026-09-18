# Especificação

Defina comportamento técnico testável e rastreável. A spec é o contrato que design, tarefas e verificação usam; ela não decide regras de negócio que pertencem ao PRD.

## Edição

Edite a spec no mesmo arquivo, sem campos de status, aprovação ou notas de ferramentas; o Git guarda evolução e autoria. Logo abaixo do título, declare o prefixo na linha ``Requirement prefix: `EXM`.`` e cite o PRD usado como origem.

Quando o PRD mudar, revise os requisitos da spec que citam os IDs alterados.

## Origem do contrato

| Origem | Evidência e cuidado |
| --- | --- |
| PRD | Cite os IDs pertinentes e preserve hipóteses e lacunas herdadas |
| Pedido direto | Registre o comportamento, consumidor e resultado informados; esclareça apenas lacunas indispensáveis |
| Código existente | Descreva comportamento observado; identifique intenção inferida e divergências com `arquivo:linha` |

Um pedido técnico delimitado dispensa PRD. Se faltar uma decisão real de produto, registre-a e continue o que independe dela. Leia a spec existente, os ADRs pertinentes e o código atingido antes de perguntar sobre o que o repositório já responde.

## Rastreabilidade do PRD

- Descreva o comportamento técnico necessário para entender e testar a regra e cite o ID de produto. A citação não substitui a explicação; evite criar uma definição de negócio concorrente.
- Preserve identificadores de estados, eventos e enumerações do domínio.
- Uma lacuna de negócio não vira hipótese técnica para permitir a implementação. Mantenha a origem explícita e bloqueie somente os requisitos dependentes.
- Escolha um prefixo técnico distinto dos prefixos de produto e das outras specs. Preserve prefixos existentes; semelhança de letras, por si só, não exige renomeação.
- Consulte a visão geral de produto, quando existir, para produtores, consumidores, direção dos contratos e decisões delegadas a ADR.
- NFR com resultado verificável gera requisito técnico ou critério de aceitação; atributos usados para comparar soluções entram como critérios de design, com origem registrada.
- Os casos de aceitação do PRD atingidos pela mudança entram na rastreabilidade pelo nome. Marque explicitamente os casos de outra capability, com seu responsável. Aceitação e rejeição são resultados distintos.

## Esclarecer o comportamento

Inspecione contratos e uma implementação pertinente antes de perguntar. Resolva escolhas técnicas reversíveis dentro da autorização; uma dúvida que exige decisão de negócio ou muda materialmente o escopo precisa da resposta do usuário. Registre a resposta no artefato correspondente.

## Superfícies expostas

Cada tipo de superfície carrega as mesmas decisões toda vez que aparece, e por isso elas se encontram percorrendo a linha em vez de lembrando. Percorra as superfícies que a mudança expõe e registre onde cada decisão aterrissou: em um requisito, em comportamento que o código já garante, ou em `n/a` com o motivo. O motivo é obrigatório porque é ele que separa uma decisão inaplicável de uma que ninguém tomou.

| Superfície | Decisões que ela sempre carrega |
| --- | --- |
| Tela ou visão | estados vazio, de carregamento, de erro e de não autorizado; ordenação e densidade; o que uma ação destrutiva confirma antes de executar |
| API ou webhook consumido de fora | formato da resposta, formato do erro e seus códigos, quem pode chamar, versionamento, comportamento no limite de taxa |
| Comando ou tarefa agendada | formato e verbosidade da saída, cada flag e seu default, exit codes, o que registra ao falhar no meio |
| Documento ou texto lido por alguém | estrutura, profundidade e a ação esperada do leitor |
| Coleção organizada | critério de agrupamento, nomeação, ordenação, tratamento de duplicatas e a exceção que não se encaixa |

Duas dessas se escondem melhor que as outras: o formato de erro é decidido por quem escreve o primeiro handler e depois copiado, e o estado vazio só aparece para quem tem conta nova. Uma mudança sem superfície exposta registra isso em uma linha.

## Dimensões do sistema

Percorra validação e limites, falha e falha parcial, idempotência e duplicação, autorização e limite de taxa, concorrência e ordenação, ciclo de vida dos dados, falha de dependência externa, transições de estado, observabilidade e consistência entre contextos. Cada uma aterrissa em requisito, em garantia que o código já oferece com a citação correspondente, ou em `n/a` com o motivo. Registre a aterrissagem: uma lista sem registro não distingue a dimensão coberta da esquecida.

A aterrissagem precisa observar aquela dimensão. Reaproveitar o requisito de outra linha é o sinal de que a dimensão continua descoberta: uma duplicata rejeitada porque a linha já existe não diz nada sobre duas requisições chegando ao mesmo tempo. Ao perceber o empréstimo, as respostas honestas são `n/a` com o motivo ou uma pergunta.

Inclua apenas requisitos justificados pela mudança, sem ampliar o produto preventivamente. Uma dimensão que depende de decisão de produto vira pergunta, não requisito inventado. O registro das duas enumerações vive na seção `Observable` da spec.

## Requisitos EARS

Use EARS para tornar claras as condições de requisitos técnicos novos quando o formato ajudar. Preserve uma formulação existente igualmente verificável. As palavras-chave seguem o idioma da spec, como o corpo: em inglês, use a coluna Forma; em português, a última coluna, com as palavras-chave em maiúsculas.

| Padrão | Forma | Adaptação em português |
| --- | --- | --- |
| Geral | The system SHALL `<resultado>` | O sistema `DEVE` produzir o resultado |
| Evento | WHEN `<gatilho>` THEN the system SHALL `<resultado>` | `QUANDO` ocorrer o gatilho, `ENTÃO` o sistema `DEVE` produzir o resultado |
| Estado | WHILE `<estado>` the system SHALL `<resultado>` | `ENQUANTO` o estado estiver ativo, o sistema `DEVE` manter o comportamento |
| Funcionalidade opcional | WHERE `<funcionalidade presente>` the system SHALL `<resultado>` | `CASO` a funcionalidade esteja presente, o sistema `DEVE` cumprir a condição |
| Condição indesejada | IF `<condição>` THEN the system SHALL `<resposta>` | `SE` ocorrer a condição, `ENTÃO` o sistema `DEVE` responder como definido |
| Composto | WHILE `<estado>`, WHEN `<gatilho>` the system SHALL `<resultado>` | `ENQUANTO` o estado estiver ativo, `QUANDO` ocorrer o gatilho, o sistema `DEVE` produzir o resultado |

Um requisito tem ID estável e uma unidade verificável. Obrigações independentes são separadas; uma condição conjunta com efeito indivisível permanece junta. Descreva estado, mensagem, valor, evento ou limite observável. Não invente HTTP status, prazo ou mecanismo para preencher a forma. Uma revisão editorial preserva comparadores, negações e permissões.

Uma única execução precisa decidir o requisito. Percentil, média, taxa de erro e disponibilidade são alvos de serviço, que nenhuma execução isolada satisfaz ou reprova; separe a linha, com o comportamento no requisito e o alvo na dimensão de observabilidade. Fundidas, a metade verificável se esconde atrás da outra e um teste que nunca tocou o número marca a linha inteira como coberta.

Um requisito que quantifica sobre um conjunto nomeia os membros ou aponta a fonte que os enumera. "Cada status do provedor mapeia para exatamente um status local" só é verificável quando se sabe quais são os status e quem tem autoridade sobre a lista; sem isso, uma prova sobre dois membros satisfaz a frase inteira.

Uma garantia de que algo não acontece precisa de mecanismo. Nada impede por si só uma duplicata, uma segunda cobrança ou uma escrita fora de ordem, então "uma repetição não cria uma segunda solicitação" é afirmação sobre maquinário: aponte a restrição, o índice ou a transação que a sustenta, ou registre a decisão que vai criá-la. Percorra a falha que produziria o resultado proibido, porque é o caminho que ninguém imagina.

Cada resultado de aceitação deve derivar de um requisito ou decisão identificável. Um cenário tem nome, entrada, condições e resultado esperado, e cita os requisitos que verifica. Se o contrato não determina o resultado de um caso limite, registre a lacuna em vez de escolher um valor por analogia com outro caso.

## Spec viva

Ao ajustar o mesmo comportamento, preserve seu ID. Ao substituir o conceito, retire o ID e crie outro. Liste os IDs retirados na linha `Retired:` ao fim da spec, para que não sejam reutilizados; não recicle números nem elimine lacunas históricas por estética.

Uma refatoração sem mudança observável preserva os requisitos e usa os testes existentes como evidência. Não modifique a spec só para produzir um diff documental.

## Organização sugerida

| Seção | Conteúdo |
| --- | --- |
| Context | Origem, consumidor, comportamento e código pertinente |
| Scope / Out of Scope | O que entra e exclusões necessárias |
| Assumptions | Hipóteses técnicas com origem, consequência e `Confirmed?` |
| Open Questions | Decisão, responsável e requisitos bloqueados |
| Requirements | IDs e comportamento observável |
| Observable | Decisões de cada superfície e dimensão, com a aterrissagem de cada uma |
| Domain Events | Produtor, consumidores, significado e gatilho |
| Glossary | Termos técnicos; termos de negócio apontam ao PRD |
| Traceability | IDs de produto e cenários relacionados aos requisitos técnicos |
| Divergences | Na origem código, diferença entre implementação e intenção documentada |

Context e Requirements são a base; Traceability entra quando houver PRD. As demais seções dependem do conteúdo. Não imponha limites de linhas ou uma lista fechada que impeça atender ao pedido.

## Exemplo parcial

O exemplo ilustra a forma; `EXM` e `PRX` são prefixos didáticos.

```markdown
Requirement prefix: `EXM`.

## Requirements

- **EXM-01** — QUANDO o consumidor repetir uma solicitação com a mesma chave e o mesmo conteúdo, ENTÃO o sistema DEVE retornar o resultado original sem criar uma segunda solicitação [PRX-01]
- **EXM-02** — SE a chave já estiver associada a outro conteúdo, ENTÃO o sistema DEVE informar conflito e preservar a solicitação original [PRX-02]

## Traceability

| ID do PRD | Requisitos |
| --- | --- |
| PRX-01 | EXM-01 |
| PRX-02 | EXM-02 |
```

Na entrega real, use os valores e erros definidos pelas fontes.
