---
name: sdd
description: Especifica, planeja, implementa, verifica ou retoma mudanças com requisitos rastreáveis da spec ao teste, e registra ADRs. Use para spec de funcionalidade ou de comportamento do sistema, inclusive a partir de necessidade de produto, pedido de tela ou CRUD, documento de produto ou código existente; para plano com decisões técnicas e tarefas; para implementação não trivial a partir de uma spec e verificação contra ela; e para ADR de decisão arquitetural nova ou já adotada no código. Não use para code review sem spec, documentação geral ou ajuste mecânico.
---

# Desenvolvimento por especificação

Converta uma necessidade em uma mudança verificável. A spec define o comportamento que o consumidor observa, inclusive as regras de negócio; o plano, a solução e as tarefas.

```mermaid
flowchart TD
    Source[Necessidade de produto, pedido técnico<br/>ou código existente] --> Spec[Spec: comportamento e regras]
    Spec --> NeedPlan{Há decisão técnica com alternativa real,<br/>decisão irreversível ou trabalho<br/>que atravessa sessões ou executores?}
    NeedPlan -- sim --> Plan[Plano: decisões e tarefas]
    NeedPlan -- não --> Short[Plano curto na conversa]
    Plan -. regra para outras capabilities .-> ADR[ADR]
    Decision[Decisão arquitetural avulsa] --> ADR
    Plan --> Execute[Execução]
    Short --> Execute
    Execute --> Verify[Verificação contra spec e plano]
    Verify -- defeito de contrato --> Fix[Corrigir na origem:<br/>spec ou plano]
```

## Escolher a etapa

Leia o [fluxo comum](references/workflow.md) e a referência da etapa solicitada. Carregue outras referências apenas quando forem pré-requisitos reais.

| Pedido | Referência | Resultado |
| --- | --- | --- |
| Especificar comportamento, inclusive a partir de necessidade de produto, ou documentar módulo existente | [Especificação](references/specify.md) | Spec com requisitos verificáveis e o custo das decisões |
| Planejar a solução e decompor o trabalho | [Plano e tarefas](references/tasks.md) | Decisões com custo e tarefas executáveis por dependência |
| Implementar spec ou funcionalidade não trivial | [Execução](references/execute.md) | Mudança implementada e verificada |
| Verificar implementação | [Verificação](references/verify.md) | Evidências de conformidade e lacunas |
| Retomar mudança | Seção Retomar uma mudança de [execução](references/execute.md) | Próxima etapa sustentada pelo estado atual |
| Registrar decisão arquitetural, avulsa ou durante o planejamento | [ADR](references/adr.md) | Decisão e consequências rastreáveis |
| Revisar spec, plano ou ADR | Referência da etapa do artefato | Achados com a regra violada |

Consulte [prosa](references/prose.md) sempre que escrever.

Os exemplos das referências são didáticos. Seus números, atores, interfaces, comandos e escolhas não se tornam fatos do projeto nem evidência executada.

Para uma correção localizada, leia o trecho e suas dependências em vez de reler todo o método, e preserve os requisitos e formatos existentes.
