---
name: prd
description: Cria e revisa PRDs de produto ou funcionalidade, inclusive de produto existente e de plataforma, SDK ou API como produto. Use para problema, usuário, comportamento, requisitos e critérios de aceitação, mesmo quando o pedido chega como tela ou CRUD; não use para spec técnica, design, tarefas, ADR ou documentação geral.
---

# Requisitos de produto

Entregue um PRD que explique o problema, o usuário afetado, o comportamento esperado, os requisitos verificáveis e os custos das decisões. Uma iniciativa técnica precisa de PRD quando muda o resultado, a informação ou o prazo que o consumidor observa. Refatoração interna, decisão arquitetural e contrato de API sem contexto de produto seguem o trabalho técnico pertinente.

## Escolher a leitura

Leia apenas as referências necessárias ao pedido; os caminhos desta tabela partem da pasta da skill.

| Pedido | Referências | Entrega |
| --- | --- | --- |
| Criar PRD | [Entrada e pesquisa](references/intake.md), [requisitos e seções](references/writing.md), [convenções](references/conventions.md), [revisão](references/workflow.md) | PRD e decisões pendentes identificadas |
| Editar PRD | Documento atual, regras pertinentes de [redação](references/writing.md), [edição no arquivo existente](references/conventions.md#editar-no-mesmo-arquivo) e [revisão](references/workflow.md) | Mesmo arquivo e IDs, com o escopo pedido |
| Documentar produto existente | Referências de criação e [PRD reverso](references/modes.md#prd-reverso) | Comportamento observado separado de intenção inferida |
| Plataforma, infraestrutura, SDK ou API como produto | Referências de criação e [produto para outros times ou sistemas](references/modes.md#produto-para-outros-times-ou-sistemas) | Consumidor, contrato e métricas apropriados |
| Revisar PRD sem editar | Documento atual, [prosa](references/prose.md) e [revisão](references/workflow.md) | Achados com IDs afetados e decisões pendentes |

Consulte [prosa](references/prose.md) ao escrever ou revisar texto. O [exemplo](references/example.md) esclarece formas e cenários; leia o trecho pertinente quando necessário, sem importar suas decisões para o produto.

## Precedência

O pedido da sessão prevalece sobre as convenções do repositório, e ambos prevalecem sobre os defaults desta skill e do verificador. Convenção é a regra escrita no `CLAUDE.md` ou em outra instrução do repositório. Um padrão apenas observado em documentos existentes não obriga, mas é preservado ao editar esses documentos.

## Verificação de estrutura

Depois de criar ou alterar PRDs, execute na raiz do repositório, trocando `docs/prd` pela pasta que a convenção do repositório fixar:

Substitua `<skill-dir>` pelo caminho absoluto da pasta que contém o `SKILL.md` efetivamente carregado; os caminhos de entrada continuam relativos à raiz do projeto consumidor:

```bash
python "<skill-dir>/scripts/check_prd.py" docs/prd
```

O alcance do script e o tratamento dos achados estão na seção Verificação de estrutura de [revisão](references/workflow.md).
