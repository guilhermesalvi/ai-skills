---
name: prd
description: Cria e revisa PRDs de produto ou funcionalidade, inclusive de produto existente e de plataforma, SDK ou API como produto. Use para problema, usuário, comportamento, requisitos e critérios de aceitação, mesmo quando o pedido chega como tela ou CRUD; não use para spec técnica, design, tarefas, ADR ou documentação geral.
---

# Requisitos de produto

Entregue um PRD que explique o problema, o usuário afetado, o comportamento esperado, os requisitos verificáveis e o custo das decisões tomadas.

Uma iniciativa técnica precisa de PRD quando muda o resultado, a informação ou o prazo que o consumidor observa. Refatoração interna, decisão arquitetural e contrato de API sem contexto de produto seguem pelo trabalho técnico, não por aqui.

## Escolher a leitura

Leia as referências cujo gatilho o pedido aciona; um pedido pode acionar várias. Os caminhos partem da pasta desta skill.

| Referência | Quando ler | O que entrega |
| --- | --- | --- |
| [Entrada e pesquisa](references/intake.md) | Ao criar um PRD, ou ao incorporar material de descoberta ou fato externo | Recorte do pedido, suficiência da informação, peso das fontes e regras de pesquisa |
| [Requisitos e seções](references/writing.md) | Ao criar um PRD; ao editar, nas regras que a mudança toca | Marcação de fatos e incertezas, capacidade de produto, fronteiras e eventos, forma dos requisitos, diagramas e seções |
| [Convenções](references/conventions.md) | Ao criar ou editar um PRD | Caminho e numeração, conteúdo admitido, edição no mesmo arquivo, cabeçalho, IDs e nomes de seção por idioma |
| [Prosa](references/prose.md) | Ao escrever ou revisar texto | Regras de redação e o que uma revisão editorial preserva |
| [Produção e revisão](references/workflow.md) | Ao criar, editar ou revisar um PRD | Verificador, conferência de estrutura, revisão de conteúdo e conteúdo da entrega |
| [Modos](references/modes.md) | Quando o PRD documenta produto existente, atende outros times ou sistemas (plataforma, infraestrutura, SDK, API) ou é a visão geral 0000 | Ajustes de evidência, seções e estrutura de cada modo |
| [Exemplo](references/example.md) | Quando a forma de um artefato não estiver clara; leia só o trecho pertinente | PRD de capability e exemplo de edição. Números, atores e decisões são fictícios: não os importe para o produto real |

## Precedência

Quando as fontes conflitarem, vale esta ordem:

1. O pedido da sessão.
2. A convenção do repositório, isto é, a regra escrita no `CLAUDE.md` ou em outra instrução do repositório.
3. Os defaults desta skill e do verificador.

Um padrão apenas observado em documentos existentes não obriga nada, mas preserve-o ao editar esses documentos.
