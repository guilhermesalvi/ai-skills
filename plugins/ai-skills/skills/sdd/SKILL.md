---
name: sdd
description: Especifica, projeta, decompõe, implementa, verifica ou retoma mudanças técnicas com requisitos rastreáveis. Use para tech spec ou spec de comportamento do sistema, design de solução, plano de tarefas, implementação não trivial a partir de uma spec e verificação contra ela; não use para PRD, ADR avulso, code review sem spec ou ajuste mecânico.
---

# Desenvolvimento por especificação

Converta os requisitos em uma mudança verificável: a spec define o comportamento técnico; o design, a solução; as tarefas, as dependências; a execução implementa; a verificação confronta o resultado com o contrato. As regras de negócio continuam no PRD responsável.

## Escolher a etapa

Leia o [fluxo comum](references/workflow.md) e a referência da etapa solicitada. Carregue outras referências quando forem pré-requisitos reais.

| Pedido | Referência | Resultado |
| --- | --- | --- |
| Especificar comportamento ou documentar módulo existente | [Especificação](references/specify.md) | Spec com critérios verificáveis |
| Projetar solução | [Design](references/design.md) | Responsabilidades, contratos, alternativas e custos |
| Decompor o trabalho | [Tarefas](references/tasks.md) | Unidades executáveis por dependência |
| Implementar spec ou funcionalidade não trivial | [Execução](references/execute.md) | Mudança implementada e verificada |
| Verificar implementação | [Verificação](references/verify.md) | Evidências de conformidade e lacunas |
| Retomar mudança | [Retomada](references/execute.md#retomar-uma-mudança) | Próxima etapa sustentada pelo estado atual |
| Registrar decisão que afeta outras capabilities durante o design | [ADR](references/adr.md) | Decisão e consequências rastreáveis |

Leia [prosa](references/prose.md) ao escrever e [validação](references/validation.md) ao revisar um artefato. Exemplos são didáticos: seus números, interfaces e escolhas não se tornam fatos do projeto.

Para uma correção localizada, leia o trecho e suas dependências; não releia todo o método. Preserve os requisitos e formatos existentes.
