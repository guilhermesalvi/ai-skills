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
| **Originating Context** | RequestManagement |

Requirement prefix: `REQ`. Visão geral: [PRD 0000](0000-platform-overview.md).
```

- O contexto dono da decisão é `Originating Context`. Consumidores afetados podem aparecer como `; affects <contextos>`, com o impacto explicado em Dependencies and Risks.
- Sem vocabulário de domínio explícito, use `Module` ou `Area` no lugar de `Originating Context`.
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

Estados, motivos e outras enumerações usadas no código mantêm uma coluna `Identifier` com o nome canônico, para diferenciar o nome de exibição da identidade do conceito.

## Rótulos de contrato

Estes rótulos mantêm a forma em inglês seja qual for o idioma da prosa, porque o verificador os compara literalmente:

`Requirement prefix:`, `Originating Context`, `Module`, `Area`, `Scope`, os títulos de seção, `[ASSUMPTION]`, `[GAP]`, `*Cost:*` e `*Reason:*`.

## Idioma

A prosa segue o idioma fixado pelo pedido ou pela convenção do repositório. Sem essa definição, use o idioma do material de origem ou, sem material, o do pedido. Mantenha a escolha nas revisões seguintes.

Termos técnicos estabelecidos podem permanecer em inglês quando a tradução perder precisão. Isso não autoriza impor frases em inglês como `if false` à prosa em português: explique diretamente a condição e seu impacto.
