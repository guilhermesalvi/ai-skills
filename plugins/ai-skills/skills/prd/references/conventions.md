# Convenções dos PRDs

Esta referência define destino, cabeçalho, IDs, rótulos e idioma dos PRDs. O que a convenção do repositório fixar sobre esses pontos prevalece.

## Caminho e numeração

Salve em `docs/prd/NNNN-<contexto>-<capability>.md`, com slugs em inglês e kebab-case. Confira os arquivos existentes e use o próximo número livre; numa pasta vazia, comece em `0001`. A visão geral usa `0000-<slug>-overview.md` e o marcador `<!-- prd: overview -->` na primeira linha, antes do título.

Um número pertence a um documento. Se uma integração produzir colisão, atribua um número livre ao novo documento, atualize quem o referencia e confira os links. A revisão de um documento existente mantém seu número.

## Editar no mesmo arquivo

O PRD é a fonte canônica do contrato de produto: propósito, escopo, comportamento e requisitos. Não registre andamento da implementação nem encaminhe o leitor ao README da solução técnica; status de desenvolvimento e mecanismos de implementação pertencem ao trabalho técnico.

Edite o PRD no próprio arquivo. O diff registra a mudança e o histórico Git registra autoria e evolução. Instruções ao agente, histórico de revisões editoriais, exemplos didáticos, campos de aprovação, status de validação e notas de ferramentas ficam fora do documento de produto.

Antes de alterar ou retirar um requisito ou caso de aceitação, procure com `git grep -n` seus IDs e o nome do caso, e confira documentos e testes dependentes.

## Cabeçalho

Uma capability apresenta título, contexto de origem e prefixo. O contexto dono da decisão é `Originating Context`; consumidores afetados podem aparecer como `; affects <contextos>`, com o impacto explicado em Dependencies and Risks. Sem vocabulário de domínio explícito, use `Module` ou `Area` no lugar de `Originating Context`. A visão geral usa `Scope` e não tem linha de prefixo nem requisitos.

```markdown
# Ciclo de uma solicitação

| | |
| --- | --- |
| **Originating Context** | RequestManagement |

Requirement prefix: `REQ`. Visão geral: [PRD 0000](0000-platform-overview.md).
```

Quando houver visão geral, a linha do prefixo tem um link para ela. Escolha o prefixo conferindo os documentos existentes.

## IDs

Use `<PREFIX>-nn` nos requisitos funcionais e `<PREFIX>-NFR-nn` nos não funcionais, com dois ou mais dígitos e um prefixo exclusivo por PRD. Não limite a numeração a 99. Toda referência precisa resolver para a definição correta.

```markdown
- **REQ-01 (Must)** Quando a solicitação for aceita, o sistema informa seu identificador ao solicitante.
- **REQ-NFR-01** O resultado deve respeitar o limite de latência definido para o contrato público.
```

O segundo exemplo só estará pronto para implementação quando o limite e sua unidade estiverem definidos; não os invente. Os requisitos funcionais levam prioridade MoSCoW (Must, Should, Could, Won't); NFRs não levam prioridade. Não reutilize IDs retirados nem renumere lacunas existentes por estética.

Estados, motivos e outras enumerações usadas no código mantêm uma coluna `Identifier` com o nome canônico. Diferencie o nome de exibição da identidade do conceito.

## Rótulos de contrato

São rótulos de contrato: `Requirement prefix:`, `Originating Context`, `Module`, `Area`, `Scope`, os títulos da tabela de seções, `[ASSUMPTION]`, `[GAP]`, `*Cost:*` e `*Reason:*`. Eles mantêm a forma em inglês seja qual for o idioma da prosa, porque o verificador os compara literalmente.

## Idioma

A prosa segue o idioma fixado pelo pedido ou pela convenção do repositório. Sem essa definição, use o idioma do material de origem ou, sem material, o do pedido, e mantenha-o nas revisões seguintes.

Termos técnicos estabelecidos podem permanecer em inglês quando a tradução perder precisão. Não imponha frases em inglês como `if false` à prosa em português; explique diretamente a condição e seu impacto.
