# Especificação

Defina comportamento técnico testável e rastreável. A spec é o contrato que design, tarefas e verificação usam; ela não decide regras de negócio, que pertencem ao PRD.

## Origem do contrato

| Origem | Evidência e cuidado |
| --- | --- |
| PRD | Cite os IDs pertinentes e preserve hipóteses e lacunas herdadas |
| Pedido direto | Registre o comportamento, consumidor e resultado informados; esclareça apenas lacunas indispensáveis |
| Código existente | Descreva comportamento observado; identifique intenção inferida e divergências com `arquivo:linha` |

Um pedido técnico delimitado dispensa PRD. Se faltar uma decisão real de produto, registre-a e continue o que independe dela.

## Rastreabilidade do PRD

- **Explique, não apenas cite.** Descreva o comportamento técnico necessário para entender e testar a regra, sem criar uma definição de negócio concorrente, e cite o ID de produto entre colchetes ao fim do requisito.
- **Preserve identificadores** de estados, eventos e enumerações do domínio.
- **Não converta lacuna de negócio em hipótese técnica** para liberar a implementação. Mantenha a origem explícita e bloqueie somente os requisitos dependentes.
- **Consulte a visão geral de produto**, quando existir, para produtores, consumidores, direção dos contratos e decisões delegadas a ADR.
- **Trate os NFRs pelo que eles permitem verificar.** NFR com resultado verificável gera requisito técnico ou critério de aceitação; atributo usado para comparar soluções entra como critério de design, com origem registrada.
- **Traga pelo nome os casos de aceitação** do PRD atingidos pela mudança, e marque os de outra capability com seu responsável. Casos de aceitação e de rejeição são cenários distintos.

## Esclarecer o comportamento

Leia a spec existente, os ADRs pertinentes, os contratos e o código atingido antes de perguntar. Resolva as escolhas técnicas reversíveis dentro da autorização; uma dúvida que exige decisão de negócio ou muda materialmente o escopo precisa da resposta do usuário. Registre a resposta no artefato correspondente.

Considere as dimensões aplicáveis: validação, falha parcial, idempotência, duplicação, autorização, concorrência, ordenação, retenção, observabilidade, dependências externas, integridade de estados e consistência entre contextos.

Inclua apenas os requisitos justificados pela mudança, sem ampliar o produto preventivamente.

## Requisitos EARS

Use EARS para tornar claras as condições de requisitos técnicos novos quando o formato ajudar. Preserve uma formulação existente que já seja igualmente verificável.

As palavras-chave seguem o idioma da spec: em inglês, use a coluna Forma; em português, a última coluna, com as palavras-chave em maiúsculas.

| Padrão | Forma | Adaptação em português |
| --- | --- | --- |
| Geral | The system SHALL `<resultado>` | O sistema `DEVE` produzir o resultado |
| Evento | WHEN `<gatilho>` THEN the system SHALL `<resultado>` | `QUANDO` ocorrer o gatilho, `ENTÃO` o sistema `DEVE` produzir o resultado |
| Estado | WHILE `<estado>` the system SHALL `<resultado>` | `ENQUANTO` o estado estiver ativo, o sistema `DEVE` manter o comportamento |
| Funcionalidade opcional | WHERE `<funcionalidade presente>` the system SHALL `<resultado>` | `CASO` a funcionalidade esteja presente, o sistema `DEVE` cumprir a condição |
| Condição indesejada | IF `<condição>` THEN the system SHALL `<resposta>` | `SE` ocorrer a condição, `ENTÃO` o sistema `DEVE` responder como definido |
| Composto | WHILE `<estado>`, WHEN `<gatilho>` the system SHALL `<resultado>` | `ENQUANTO` o estado estiver ativo, `QUANDO` ocorrer o gatilho, o sistema `DEVE` produzir o resultado |

Um requisito tem ID estável e representa uma unidade verificável. Obrigações independentes ficam separadas; uma condição conjunta com efeito indivisível permanece junta.

Descreva estado, mensagem, valor, evento ou limite observável. Não invente HTTP status, prazo ou mecanismo para preencher a forma.

## Cenários de aceitação

Cada resultado de aceitação deriva de um requisito ou decisão identificável. Um cenário tem nome, entrada, condições e resultado esperado, e cita os requisitos que verifica.

Se o contrato não determinar o resultado de um caso limite, registre a lacuna em vez de escolher um valor por analogia com outro caso.

## Arquivo, prefixo e IDs

Edite a spec no mesmo arquivo, sem campos de status, aprovação ou notas de ferramentas: o Git já guarda evolução e autoria.

Logo abaixo do título, declare o prefixo na linha ``Requirement prefix: `EXM`.`` e cite o PRD usado como origem. O prefixo técnico é distinto dos prefixos de produto e das outras specs. Preserve prefixos existentes; semelhança de letras, por si só, não exige renomeação.

Ao ajustar o mesmo comportamento, preserve o ID dele. Ao substituir o conceito, retire o ID e crie outro. Liste os IDs retirados na linha `Retired:` ao fim da spec, para que não sejam reutilizados, e não elimine lacunas históricas por estética.

Quando o PRD mudar, revise os requisitos da spec que citam os IDs alterados.

Uma refatoração sem mudança observável preserva os requisitos e usa os testes existentes como evidência. Não modifique a spec só para produzir um diff documental.

## Organização sugerida

Context e Requirements são a base; Traceability entra quando houver PRD, e as demais seções dependem do conteúdo.

| Seção | Conteúdo |
| --- | --- |
| Context | Origem, consumidor, comportamento e código pertinente |
| Scope / Out of Scope | O que entra e exclusões necessárias |
| Assumptions | Hipóteses técnicas com origem e consequência |
| Open Questions | Decisão, responsável e requisitos bloqueados |
| Requirements | IDs e comportamento observável |
| Domain Events | Produtor, consumidores, significado e gatilho |
| Glossary | Termos técnicos; termos de negócio apontam ao PRD |
| Traceability | IDs de produto e cenários relacionados aos requisitos técnicos |
| Divergences | Na origem código, diferença entre implementação e intenção documentada |

## Exemplo parcial

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
