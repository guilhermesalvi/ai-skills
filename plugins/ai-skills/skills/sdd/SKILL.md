---
name: sdd
description: Especifique comportamentos completos, prepare, implemente e verifique mudanças com requisitos rastreáveis. Use para specs a partir de produto ou código, planos técnicos, implementação por spec e ADRs. Não use para code review sem spec, documentação geral ou ajustes mecânicos.
---

# Desenvolvimento por especificação

Converta o pedido, o material de produto ou o código existente em um contrato verificável. Entregue os artefatos e as etapas que o pedido autoriza.

| Artefato | Resultado |
| --- | --- |
| Spec | Contrato vivo de um comportamento completo, do gatilho ao resultado observável, com requisitos estáveis |
| Plano | Decisões técnicas, checks e, quando necessário, organização da execução |
| ADR | Decisão arquitetural e seus custos, aplicável a múltiplos comportamentos ou pedida como registro avulso |

## Escolher as referências

Leia o [fluxo comum](references/workflow.md) ao iniciar o trabalho com a skill. Depois, escolha as referências pelo resultado pedido. Reutilize as que já estiverem no contexto; uma correção localizada exige apenas o trecho pertinente e suas dependências.

| Referência | Quando ler |
| --- | --- |
| [Prosa](references/prose.md) | Ao escrever ou revisar qualquer artefato |
| [Alterar artefato](references/change.md) | Ao alterar requisitos ou cenários existentes, resolver colisões de numeração entre branches ou revisar uma spec, um plano ou um ADR |
| [Especificação](references/specify.md) | Ao criar ou revisar uma spec, inclusive a partir de produto ou código |
| [Exemplo de spec](references/spec-example.md) | Quando houver dúvida sobre a aplicação do schema ou o nível de detalhe de uma spec nova |
| [Plano](references/plan.md) | Ao criar ou revisar um plano de solução |
| [Preparação](references/prepare.md) | Ao avaliar se uma mudança pode ser implementada ou preparar sua passagem para outro executor |
| [Execução](references/execute.md) | Ao implementar ou retomar uma mudança, com ou sem spec e plano existentes |
| [Verificação](references/verify.md) | Ao verificar a implementação contra a spec e o plano |
| [ADR](references/adr.md) | Ao registrar ou revisar uma decisão pedida como ADR ou encaminhada pelo plano |
| [Entrega](references/deliver.md) | Ao conferir os artefatos e preparar a resposta final, em qualquer modo |

## Recursos e limites

- Resolva os caminhos a partir da pasta deste `SKILL.md`. `<skill-dir>` representa esse caminho absoluto. Os modelos ficam em `assets/`; a conferência determinística usa `scripts/check_spec.py`, com Python 3.10+ e Git, a partir do projeto consumidor.
- Trate os exemplos como ilustrações de formato. Use os fatos, interfaces e comandos do projeto ao produzir o artefato.
