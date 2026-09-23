---
name: prd
description: Cria e revisa PRDs de produto ou funcionalidade, inclusive de produto existente e de plataforma, SDK ou API como produto. Use para problema, usuário, comportamento, requisitos e critérios de aceitação, mesmo quando o pedido chega como tela ou CRUD; não use para spec técnica, design, tarefas, ADR ou documentação geral.
---

# Requisitos de produto

Entregue um PRD que explique o problema, o usuário afetado, o comportamento esperado, os requisitos verificáveis e o custo das decisões tomadas.

Uma iniciativa técnica precisa de PRD quando muda o resultado, a informação ou o prazo que o consumidor observa. Refatoração interna, decisão arquitetural e contrato de API sem contexto de produto seguem pelo trabalho técnico, não por aqui.

## Escolher a leitura

Leia apenas as referências que o pedido exige. Os caminhos partem da pasta desta skill.

| Pedido | Referências | Entrega |
| --- | --- | --- |
| Criar PRD | [Entrada e pesquisa](references/intake.md), [requisitos e seções](references/writing.md), [convenções](references/conventions.md), [produção e revisão](references/workflow.md) | PRD e decisões pendentes identificadas |
| Editar PRD | Documento atual, regras pertinentes de [requisitos e seções](references/writing.md), seção Editar no mesmo arquivo de [convenções](references/conventions.md) e [produção e revisão](references/workflow.md) | Mesmo arquivo e IDs, com o escopo pedido |
| Documentar produto existente | Referências de criação e seção PRD reverso de [modos](references/modes.md) | Comportamento observado separado de intenção inferida |
| Plataforma, infraestrutura, SDK ou API como produto | Referências de criação e seção Produto para outros times ou sistemas de [modos](references/modes.md) | Consumidor, contrato e métricas apropriados |
| Visão geral de várias capabilities (PRD 0000) | Referências de criação e seção Visão geral de [modos](references/modes.md) | Contextos, eventos e fluxos entre capabilities |
| Revisar PRD sem editar | Documento atual, [prosa](references/prose.md) e [produção e revisão](references/workflow.md) | Achados com IDs afetados e decisões pendentes |

Consulte [prosa](references/prose.md) sempre que escrever ou revisar texto.

O [exemplo](references/example.md) mostra a forma dos artefatos. Leia o trecho pertinente quando a forma não estiver clara. Seus números, atores e decisões são fictícios: não os importe para o produto real.

## Precedência

Quando as fontes conflitarem, vale esta ordem:

1. O pedido da sessão.
2. A convenção do repositório, isto é, a regra escrita no `CLAUDE.md` ou em outra instrução do repositório.
3. Os defaults desta skill e do verificador.

Um padrão apenas observado em documentos existentes não obriga nada, mas preserve-o ao editar esses documentos.
