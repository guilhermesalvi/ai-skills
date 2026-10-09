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

- Para uma mudança simples, use as decisões e os checks do plano diretamente. Não acrescente uma decomposição que só repita essas informações.
- Numa alteração localizada em um componente, omita Execution salvo pedido de decomposição ou passagem de trabalho, ou dependência de implementação ainda não expressa nos demais registros. Implementar e depois rodar o gate não justifica a seção: a verificação final já faz parte da execução do plano.
- Use Execution no plano quando dependências, entregas por partes ou passagem entre executores exigirem contexto ou ordem que os demais registros não deixem claros. Omita a seção quando ela apenas nomear etapas dedutíveis das decisões e dos checks.
- Organize cada item por resultado implementável e verificável, com sua prova. Separar código e testes do mesmo resultado em itens sequenciais não prepara uma entrega integrada. Uma etapa intermediária pode ser necessária para integrar o comportamento completo; não a transforme numa spec isolada.
- Dê ao item um nome local em inglês e kebab-case. Esses nomes organizam o plano; não são novos IDs de requisito.
- Registre dependências pelos nomes dos itens, separados por vírgula, ou `none`. Não crie dependência só para impor uma sequência preferida. Não permita ciclos ou dependência de si próprio.
- Em Context, cite as fontes e os contratos que o item precisa, as convenções pertinentes e as premissas ou lacunas que o afetam. Se necessário, acrescente explicação abaixo da tabela. Um catálogo de arquivos sem explicar sua pertinência não prepara o executor.
- Em Checks, cite o ID do requisito, o nome da decisão técnica ou `Gate`, conforme os checks existentes. Não copie comandos nem resultados esperados da seção Checks. Um item pode citar vários checks, e o mesmo check pode observar a integração de vários itens.
- Registre em Outcome o resultado cuja prova permite considerar o item integrado; escrever o código ou passar uma parte isolada não comprova o comportamento completo.

O schema de Execution e seu modelo estão no [plano](plan.md#execution). A tabela orienta dependências e passagem de contexto; não obriga agentes adicionais, execução paralela nem uma quantidade fixa de itens.

## Ajustar com novas evidências

Quando uma descoberta alterar uma dependência, decisão ou prova, atualize os registros afetados antes de continuar o trabalho que usa essa informação. Preserve os itens e as evidências ainda válidos. Corrija o contrato na origem, conforme o fluxo comum, sem redefinir o resultado de negócio por conta própria.

Na passagem para outra sessão, confira Execution, quando presente, e registre em Progress a fronteira alcançada e a evidência que sustenta o próximo trabalho. A retomada segue [execução](execute.md#retomar-uma-mudança).
