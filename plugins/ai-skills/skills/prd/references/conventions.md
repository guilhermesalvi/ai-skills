# Convenções dos PRDs

## Caminho e numeração

Salve em `docs/prd/NNNN-<contexto>-<capability>.md`, com slugs em inglês e em kebab-case. Confira os arquivos existentes e use o próximo número livre; numa pasta vazia, comece em `0001`, porque `0000` é reservado à visão geral.

Um número pertence a um documento. Se uma integração produzir colisão, atribua um número livre ao novo documento, atualize quem o referencia e confira os links. A revisão de um documento existente mantém o número dele.

## Conteúdo do documento

O PRD é a fonte canônica do contrato de produto: propósito, escopo, comportamento e requisitos. Status de desenvolvimento e mecanismos de implementação pertencem ao trabalho técnico, então não registre andamento da implementação nem encaminhe o leitor ao README da solução técnica.

Ficam fora do documento as instruções ao agente, o histórico de revisões editoriais, os exemplos didáticos, os campos de aprovação, o status de validação e as notas de ferramentas.

## Editar no mesmo arquivo

Edite o PRD no próprio arquivo: o diff registra a mudança e o histórico Git registra autoria e evolução.

Antes de alterar ou retirar um requisito ou um caso de aceitação, procure com `git grep -n` pelos IDs e pelo nome do caso, e confira documentos e testes dependentes.

## Cabeçalho

Uma capability apresenta título, contexto de origem e prefixo:

```markdown
# Ciclo de uma solicitação

| | |
| --- | --- |
| **Contexto de origem** | RequestManagement |

Prefixo dos requisitos: `REQ`. Visão geral: [PRD 0000](0000-platform-overview.md).
```

- O contexto de origem é o dono da decisão. Consumidores afetados podem aparecer como `; afeta <contextos>`, com o impacto explicado em Dependências e riscos.
- Sem vocabulário de domínio explícito, use Módulo ou Área no lugar de Contexto de origem.
- Quando houver visão geral, a linha do prefixo traz um link para ela.

Escolha o prefixo conferindo os documentos existentes.

## IDs

Use `<PREFIX>-nn` nos requisitos funcionais e `<PREFIX>-NFR-nn` nos não funcionais, com dois ou mais dígitos e um prefixo exclusivo por PRD. Não limite a numeração a 99, e garanta que toda referência resolva para a definição correta.

```markdown
- **REQ-01 (Must)** Quando a solicitação for aceita, o sistema informa seu identificador ao solicitante.
- **REQ-NFR-01** O identificador é informado em até 2 segundos após a aceitação, no percentil 95.
```

Os requisitos funcionais levam prioridade MoSCoW (Must, Should, Could, Won't); os NFRs não levam prioridade.

Um ID retirado não volta a ser usado. Como ele some do arquivo, confira com `git log -S "<ID>"` que o número nunca existiu antes de atribuí-lo. Não renumere lacunas existentes por estética.

Estados, motivos e outras enumerações usadas no código mantêm uma coluna Identificador com o nome canônico, para diferenciar o nome de exibição da identidade do conceito.

## Idioma

A prosa segue o idioma fixado pelo pedido ou pela convenção do repositório. Sem essa definição, use o idioma do material de origem ou, sem material, o do pedido. Mantenha a escolha nas revisões seguintes; um PRD existente conserva o idioma dos seus títulos.

Títulos de seção, rótulos e tags acompanham o idioma da prosa, sem misturar idiomas no mesmo documento. Esta skill os nomeia em português; num PRD em inglês, use a coluna English da tabela abaixo, para que PRDs diferentes usem os mesmos nomes.

Termos canônicos em inglês não se traduzem em nenhum idioma: JTBD, MoSCoW (Must, Should, Could, Won't), NFR, trade-off, Leading, Lagging e Guardrails. Fora deles, termos técnicos estabelecidos podem permanecer em inglês quando a tradução perder precisão, mas isso não autoriza impor frases em inglês como `if false` à prosa em português: explique diretamente a condição e seu impacto.

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
| `; afeta <contextos>` | `; affects <contexts>` |
| `Prefixo dos requisitos:` | `Requirement prefix:` |
| Identificador | Identifier |
| `[PREMISSA]`, `[LACUNA]` | `[ASSUMPTION]`, `[GAP]` |
| `*Custo:*`, `*Motivo:*` | `*Cost:*`, `*Reason:*` |
