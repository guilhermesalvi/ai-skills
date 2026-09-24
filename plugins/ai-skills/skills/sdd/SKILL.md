---
name: sdd
description: Escreve PRDs e especifica, projeta, decompõe, implementa, verifica ou retoma mudanças técnicas com requisitos rastreáveis do produto ao código. Use para PRD de produto ou funcionalidade, inclusive de produto existente e de plataforma, SDK ou API como produto, mesmo quando o pedido chega como tela ou CRUD; para tech spec ou spec de comportamento do sistema, design de solução, plano de tarefas, implementação não trivial a partir de uma spec e verificação contra ela. Não use para ADR avulso, code review sem spec, documentação geral ou ajuste mecânico.
---

# Desenvolvimento por especificação

Converta uma necessidade em uma mudança verificável. O PRD define problema, comportamento e regras de negócio; a spec, o comportamento técnico; o design, a solução.

```mermaid
flowchart TD
    Need[Necessidade de produto] --> PRD[PRD: problema e regras de negócio]
    PRD --> Spec[Spec: comportamento técnico]
    Source[Pedido técnico ou código existente] --> Spec
    Spec --> NeedDesign{Há decisão de arquitetura, contrato público,<br/>persistência, integração ou migração,<br/>ou risco que exija comparar soluções?}
    NeedDesign -- sim --> Design[Design: solução]
    Design -. regra para outras capabilities .-> ADR[ADR]
    Design --> NeedTasks
    NeedDesign -- não --> NeedTasks{A decomposição e as dependências<br/>precisam de registro durável?}
    NeedTasks -- sim --> Tasks[Tarefas]
    NeedTasks -- não --> Plan[Plano curto na conversa]
    Tasks --> Execute[Execução]
    Plan --> Execute
    Execute --> Verify[Verificação contra spec e design]
    Verify -- defeito de contrato --> Fix[Corrigir na origem:<br/>PRD, spec ou design]
```

Uma mudança precisa de PRD quando muda o resultado, a informação ou o prazo que o consumidor observa. Refatoração interna, decisão arquitetural e contrato de API sem contexto de produto começam pela spec.

## Escolher a etapa

Leia o [fluxo comum](references/workflow.md) e a referência da etapa solicitada. Carregue outras referências apenas quando forem pré-requisitos reais.

| Pedido | Referência | Resultado |
| --- | --- | --- |
| Escrever, editar ou revisar PRD, inclusive a visão geral de produto | [PRD](references/prd.md) | Problema, usuário, comportamento, requisitos verificáveis e custo das decisões |
| Especificar comportamento ou documentar módulo existente | [Especificação](references/specify.md) | Spec com critérios verificáveis |
| Projetar solução | [Design](references/design.md) | Responsabilidades, contratos, alternativas e custos |
| Decompor o trabalho | [Tarefas](references/tasks.md) | Unidades executáveis por dependência |
| Implementar spec ou funcionalidade não trivial | [Execução](references/execute.md) | Mudança implementada e verificada |
| Verificar implementação | [Verificação](references/verify.md) | Evidências de conformidade e lacunas |
| Retomar mudança | Seção Retomar uma mudança de [execução](references/execute.md) | Próxima etapa sustentada pelo estado atual |
| Registrar decisão que afeta outras capabilities durante o design | [ADR](references/adr.md) | Decisão e consequências rastreáveis |
| Revisar spec, design, tarefas ou ADR | Referência da etapa do artefato | Achados com a regra violada |

Consulte [prosa](references/prose.md) sempre que escrever.

Os exemplos das referências são didáticos. Seus números, atores, interfaces, comandos e escolhas não se tornam fatos do projeto nem evidência executada.

Para uma correção localizada, leia o trecho e suas dependências em vez de reler todo o método, e preserve os requisitos e formatos existentes.
