# Preparação da execução

Leia esta referência antes de implementar e quando o plano precisar orientar outro executor. Prepare apenas o que falta para executar e provar o comportamento autorizado.

## Prontidão

Confira, na spec, no plano e nas fontes pertinentes:

- O gatilho e o resultado completo estão definidos, inclusive as regras e recusas que a mudança precisa atender.
- As decisões necessárias à solução estão tomadas ou registradas como premissas defensáveis, conforme o [fluxo comum](workflow.md#premissas-e-lacunas).
- Os contratos, pontos de integração e comandos usados na execução foram confirmados nas fontes; o contexto identifica o que ainda não foi verificado.
- As dependências necessárias estão disponíveis ou têm uma ordem de execução definida, e os checks observam o resultado na camada correspondente.

Uma lacuna bloqueia apenas o trabalho que depende dela. Cite o registro existente em Gaps e continue o que puder ser implementado e integrado sem decidir a lacuna. Não crie um campo de aprovação ou uma segunda lista de pendências para representar prontidão.

## Organizar o trabalho

- Use Execution no plano somente quando o pedido pedir decomposição, ou quando dependências entre partes, entrega em etapas ou passagem a outro executor exigirem contexto ou ordem que as decisões e os checks não deixem claros. Sem isso, use as decisões e os checks diretamente; implementar e depois rodar o gate não justifica a seção.
- Organize cada item por resultado implementável e verificável. Separar código e testes do mesmo resultado em itens sequenciais não prepara uma entrega integrada. Uma etapa intermediária pode ser necessária para integrar o comportamento completo; não a transforme numa spec isolada.
- Preencha a tabela conforme o [schema de Execution](plan.md#execution). Ela orienta dependências e passagem de contexto; não obriga agentes adicionais, execução paralela nem uma quantidade fixa de itens.

## Ajustar com novas evidências

Quando uma descoberta alterar uma dependência, decisão ou prova, atualize os registros afetados antes de continuar o trabalho que usa essa informação. Preserve os itens e as evidências ainda válidos. Corrija o contrato na origem, conforme o fluxo comum, sem redefinir o resultado de negócio por conta própria.

Na passagem para outra sessão, confira Execution, quando presente, e registre Progress conforme [passar a mudança adiante](execute.md#passar-a-mudança-adiante). A retomada segue [execução](execute.md#retomar-uma-mudança).
