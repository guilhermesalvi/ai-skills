---
name: sdd
description: Especifique, planeje, implemente e verifique mudanças com requisitos rastreáveis. Use para specs a partir de produto ou código, planos técnicos, implementação por spec e ADRs. Não use para code review sem spec, documentação geral ou ajustes mecânicos.
---

# Desenvolvimento por especificação

Converta o pedido, o material de produto ou o código existente em um contrato verificável. Entregue os artefatos e as etapas que o pedido autoriza.

Na própria resposta final, informe os caminhos dos artefatos, o resultado, as evidências e todas as premissas `Confirmed? n` que sustentam o escopo entregue, com os IDs afetados. Faça perguntas diretas sobre as lacunas de negócio abertas, com opções e recomendação.

| Artefato | Resultado |
| --- | --- |
| Spec | Comportamento observável da capability, com regras de negócio e requisitos estáveis |
| Plano | Decisões técnicas e checks que provam a mudança |
| ADR | Decisão arquitetural e seus custos, aplicável a outras capabilities ou pedida como registro avulso |

## Escolher as referências

Leia o [fluxo comum](references/workflow.md) ao iniciar o trabalho com a skill. Depois, escolha as referências pelo resultado pedido. Reutilize as que já estiverem no contexto; uma correção localizada exige apenas o trecho pertinente e suas dependências.

| Referência | Quando ler |
| --- | --- |
| [Prosa](references/prose.md) | Ao escrever ou revisar qualquer artefato |
| [Alterar artefato](references/change.md) | Alterar, dividir ou retirar um requisito ou cenário existente; resolver número repetido entre branches; revisar uma spec, um plano ou um ADR |
| [Especificação](references/specify.md) | Criar ou revisar uma spec, inclusive a partir de produto ou código |
| [Exemplo de spec](references/spec-example.md) | Esclarecer a aplicação do schema e o nível de detalhe de uma spec nova |
| [Plano](references/plan.md) | Planejar a solução; implementar uma mudança ainda sem plano; revisar um plano |
| [Execução](references/execute.md) | Implementar ou retomar uma mudança por spec; criar antes a spec e o plano que faltarem |
| [Verificação](references/verify.md) | Verificar a implementação contra a spec e o plano |
| [ADR](references/adr.md) | Registrar uma decisão pedida como ADR ou encaminhada pelo plano; revisar um ADR |

Ao preparar a resposta final, aplique [entrega](references/deliver.md) em qualquer modo. Confira os artefatos contra os critérios pertinentes, corrija os achados e inclua na resposta os registros que essa referência exige.

## Recursos e limites

- Resolva os caminhos a partir da pasta deste `SKILL.md`. `<skill-dir>` representa esse caminho absoluto. Os modelos ficam em `assets/`; a conferência determinística usa `scripts/check_spec.py`, com Python 3.10+ e Git, a partir do projeto consumidor.
- Trate os exemplos como ilustrações de formato. Use os fatos, interfaces e comandos do projeto ao produzir o artefato.
