# Convenções dos PRDs

## Caminho e numeração

Salve em `docs/prd/NNNN-<contexto>-<capability>.md`. `NNNN` é o número do documento, com quatro dígitos; `<contexto>` e `<capability>` são slugs em inglês e em kebab-case. Num PRD novo, use o número seguinte ao maior da pasta; numa pasta vazia, comece em `0001`, porque `0000` é reservado à visão geral.

Cada número pertence a um só documento e não muda quando o documento é revisado. Se dois documentos chegarem ao mesmo número, como ao integrar branches paralelas, mantenha o número do que já estava na branch de destino, dê ao outro o número seguinte ao maior da pasta e atualize os links que apontavam para o nome antigo.

## Conteúdo do documento

O PRD é a fonte canônica do contrato de produto: propósito, escopo, comportamento e requisitos. O andamento da implementação pertence ao trabalho técnico: não o registre no PRD nem remeta o leitor a um README ou outro documento técnico para acompanhá-lo.

Ficam fora do documento, porque não descrevem o produto:

- instruções dirigidas ao agente ou a quem edita o PRD;
- histórico de revisões, que o Git já registra;
- campos de aprovação e status do documento, como rascunho, validado ou aprovado;
- resultado das verificações e da revisão, que a entrega informa na resposta;
- notas sobre a ferramenta que gerou ou editou o texto;
- exemplos que ilustram o método de escrita em vez do comportamento do produto. Exemplos que especificam o produto, como tabelas de cálculo e casos de aceitação, continuam no documento.

## Editar no mesmo arquivo

Altere o PRD no próprio arquivo, sem criar cópia ou versão paralela: o diff registra a mudança, e o histórico do Git, a autoria e a evolução.

Antes de alterar ou retirar um requisito ou um caso de aceitação, procure seus IDs e o nome do caso com `git grep -n` para encontrar os PRDs e testes que dependem deles.

## Cabeçalho

O PRD de uma capability começa pelo título e por uma tabela de cabeçalho:

```markdown
# Emissão de fatura

| | |
| --- | --- |
| **Contexto de origem** | Invoicing |
| **Contextos afetados** | Notification, Accounting |
| **Prefixo dos requisitos** | `INV` |
| **Visão geral** | [PRD 0000](0000-platform-overview.md) |
```

- Em Contexto de origem, informe o contexto dono das regras deste PRD. Se o projeto não divide o produto em contextos de domínio, troque o rótulo por Módulo ou Área, conforme o termo que o projeto usa, e troque Contextos afetados pelo plural correspondente.
- Inclua Contextos afetados quando o PRD muda o que outros contextos recebem ou observam, e explique o impacto em Dependências e riscos. Sem contexto afetado, omita a linha.
- Inclua Visão geral quando a pasta tiver o PRD 0000; sem ele, omita a linha.

## IDs

O ID de um requisito começa pelo prefixo do PRD que o define, para que uma citação em outro PRD, numa spec ou num teste indique onde está a definição. O prefixo é uma abreviação do contexto de origem ou da capability, em letras maiúsculas e dígitos, começando por letra, como `INV` para Invoicing ou `ONB` para CustomerOnboarding. Evite nomes genéricos como `REQ`, que não indicam o dono, e não use `FR` nem `NFR`, que o verificador trata como ID sem prefixo. Num PRD novo, escolha um prefixo que nenhum PRD da pasta use e, se a pasta tiver o PRD 0000, registre o PRD e o prefixo na seção Contextos dele; ao editar, mantenha o prefixo existente.

O ID tem a forma `<PREFIX>-nn`, com uma única sequência por PRD para requisitos funcionais e não funcionais. O tipo é dado pela seção onde o requisito é definido, Requisitos funcionais ou Requisitos não funcionais, e não pelo ID; assim, reclassificar um requisito muda a seção sem mudar o ID. Numere com pelo menos dois dígitos (`01`, `02`) e, depois de `99`, siga para `100`.

Defina cada requisito num item de lista que começa pelo ID em negrito, com a prioridade MoSCoW (Must, Should, Could, Won't) entre parênteses dentro do negrito:

```markdown
## Requisitos funcionais

- **INV-01 (Must)** Quando a fatura for emitida, o sistema informa seu número ao cliente.

## Requisitos não funcionais

- **INV-02 (Should)** O número é informado em até 2 segundos após a emissão, no percentil 95.
```

Todo ID citado precisa estar definido num PRD da pasta e corresponder ao requisito que o texto pretende citar.

Um requisito novo recebe o número seguinte ao maior já usado com o mesmo prefixo. Um ID retirado some do arquivo, então confira com `git log -S "<ID>"` que o número nunca existiu antes de atribuí-lo. Um ID retirado não volta a ser usado, e os demais não são renumerados para fechar buracos na sequência.

Quando estados, motivos ou outras enumerações tiverem valores referenciados pelo código ou pelos contratos, liste-os numa tabela com a coluna Identificador ao lado do nome de exibição. O Identificador traz o nome estável do valor, como `UnderReview`, e permite mudar o nome de exibição sem mudar a identidade do conceito.

## Idioma

Num PRD novo, a prosa segue o idioma fixado pelo pedido ou pela convenção do repositório. Sem essa definição, use o idioma do material de origem ou, sem material, o idioma em que o pedido foi escrito. Títulos de seção, rótulos e tags seguem o idioma da prosa.

Ao editar um PRD existente, mantenha o idioma da prosa e o dos títulos que ele já usa, mesmo que um difira do outro: não traduza um documento existente sem pedido.

Esta skill nomeia títulos, rótulos e tags em português. Num PRD em inglês, use a coluna English da tabela abaixo; em outro idioma, traduza a coluna Português e use a mesma tradução em todos os PRDs da pasta. Assim, PRDs diferentes usam os mesmos nomes.

Termos canônicos em inglês não se traduzem em nenhum idioma: JTBD, MoSCoW (Must, Should, Could, Won't), NFR, trade-off, Leading, Lagging e Guardrails. Outros termos técnicos estabelecidos podem ficar em inglês quando a tradução perder precisão. A permissão vale para termos, não para expressões: em vez de escrever `if false` no meio da prosa, descreva a condição e o seu impacto.

| Português | English |
| --- | --- |
| Resumo executivo | Executive Summary |
| Alinhamento estratégico | Strategic Alignment |
| Contexto e problema | Context and Problem |
| Usuário-alvo / JTBD | Target User / JTBD |
| Oportunidade / hipótese | Opportunity / Hypothesis |
| Solução proposta | Proposed Solution |
| Glossário do domínio | Domain Glossary |
| Requisitos funcionais | Functional Requirements |
| Eventos de domínio | Domain Events |
| Requisitos não funcionais | Non-functional Requirements |
| Considerações regulatórias | Regulatory Considerations |
| Fora do escopo | Non-goals |
| Trade-offs declarados | Declared Trade-offs |
| Métricas de sucesso | Success Metrics |
| Critérios de aceitação | Acceptance Criteria |
| Dependências e riscos | Dependencies and Risks |
| Questões em aberto | Open Questions |
| Ponto mais frágil | Weakest Point |
| Referências | References |
| Propósito | Purpose |
| Contextos | Contexts |
| Catálogo de eventos | Event Catalog |
| Fluxos entre contextos | Flows Between Contexts |
| Termos por contexto | Terms per Context |
| Decisões delegadas a ADR | Decisions Delegated to ADR |
| Contexto de origem, Módulo, Área, Escopo | Originating Context, Module, Area, Scope |
| Contextos afetados, Módulos afetados, Áreas afetadas | Affected Contexts, Affected Modules, Affected Areas |
| Prefixo dos requisitos | Requirement Prefix |
| Visão geral | Overview |
| Identificador | Identifier |
| `[PREMISSA]`, `[LACUNA]` | `[ASSUMPTION]`, `[GAP]` |
| `*Custo:*`, `*Motivo:*` | `*Cost:*`, `*Reason:*` |
