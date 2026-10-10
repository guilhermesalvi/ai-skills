# Alterar um artefato existente

Altere e revise specs, planos e ADRs preservando a identidade dos requisitos e os documentos que dependem deles.

## Antes de alterar

- Antes de alterar ou retirar um requisito ou cenário, procure o ID do requisito ou o nome do cenário nas specs, nos planos e nos testes. Use `rg -n` ou a busca do projeto, incluindo arquivos novos ainda sem commit.

## IDs de requisito

- Ao ajustar um requisito sem substituir o conceito que ele representa, preserve o ID.
- Ao substituir o conceito, retire o ID e crie outro.
- Ao dividir um requisito, o ID fica com a parte que mantém o conceito do enunciado original, e as demais partes recebem IDs novos.
- Ao retirar um requisito, remova sua definição da spec. As specs e os planos em andamento que citavam o ID passam a citar o substituto ou deixam de citá-lo; os planos concluídos ficam como estão.
- O documento não guarda lista de IDs retirados: o histórico do Git registra o que cada ID significava.
- Um ID retirado não volta a ser usado, e os demais não são renumerados para fechar buracos na sequência.

## Resolver uma premissa

Retire a premissa de Assumptions quando houver evidência ou decisão suficiente e registre o resultado no lugar correspondente:

| Resolução | Destino e origem |
| --- | --- |
| Fato verificado | Context ou a seção que usa o fato, com a evidência que o comprova |
| Escolha decidida pelo usuário, inclusive por delegação | Requirements na spec ou Technical Decisions no plano, com a origem da decisão; registre quem decidiu e a data quando conhecidos |

- Aceitar uma inferência não comprova um fato. Mantenha a premissa aberta até verificar a afirmação.
- Atualize os requisitos e as citações que dependiam da premissa. Se ela atendia uma lacuna, resolva também o registro em Gaps. Apague Assumptions quando a seção ficar vazia.

## Observable Decisions

Siga esta seção quando a spec já tiver Observable Decisions ou o pedido exigir um mapa de decisões. O mapa localiza decisões já registradas, sem criar uma segunda definição:

| Registro | Citação em Landing |
| --- | --- |
| Requisito | ID, quando a ligação esclarece uma interação entre superfícies ou condições |
| Garantia existente no código | Arquivo, símbolo e o resultado garantido |
| Premissa | Título da premissa |
| Lacuna | Texto da coluna Gap |

- Ao alterar a spec, percorra as superfícies e as [dimensões](specify.md#dimensões) que a mudança expõe e atualize as linhas que ela atinge.
- Cite em cada linha apenas requisitos que observam aquela dimensão; um requisito pode aparecer em várias linhas.
- Em Landing, cite apenas o ID ou o nome do registro que já contém a decisão. Descreva somente a garantia externa que não está em outro registro.
- Vincule a uma premissa ou lacuna a dimensão aplicável que ainda não tiver requisito.
- Mantenha só as linhas que acrescentam uma ligação ou garantia necessária para entender o contrato; remova a que apenas indexa um registro já claro. Sem linha útil, remova a seção.
- Preserve uma linha `n/a` existente enquanto o motivo for útil, no formato `<Dimension>: <motivo>`, com entradas separadas por ponto e vírgula; não a crie para completar a lista. O motivo não cita requisito: se um requisito observa a dimensão, ela se aplica e tem linha própria.

## Dividir uma spec abrangente

Quando a manutenção ou o pedido justificar a divisão, identifique comportamentos completos e os consumidores dos requisitos antes de mover o contrato. Mova cada definição para uma única fonte, preserve seu ID e atualize os links e as citações dos consumidores em andamento. Não mantenha cópias da regra nas specs de origem e destino.

Preserve os prefixos e os IDs existentes: cada spec tem um prefixo e cada prefixo pertence a uma única spec. Se a divisão exigir distribuir o mesmo prefixo entre arquivos, mantenha o contrato existente como fonte e referencie suas regras nos novos comportamentos. Uma migração de IDs precisa de escopo explícito e atualização dos consumidores; não renumere por conveniência.

## Número repetido entre branches

- Quando branches paralelos criarem planos ou ADRs com o mesmo número na mesma pasta, ou requisitos distintos com o mesmo ID, preserve o número ou ID do item que já estava na branch de destino. Renumere o item da outra branch conforme Numeração ou IDs novos do [fluxo comum](workflow.md), de acordo com o tipo de item, e atualize suas citações.

## Revisar um artefato

Numa revisão de spec, plano ou ADR, com profundidade proporcional à mudança, confira:

- Caminhos, links e IDs resolvem para as fontes corretas; a numeração não colide; IDs retirados não voltam.
- Idioma, títulos e formato existentes foram preservados, e cada seção tem conteúdo útil.
- Nenhum placeholder finge que uma decisão foi tomada, e nenhum exemplo aparece como evidência executada.
- Diagramas têm estrutura coerente, e o relatório diferencia inspeção textual de renderização.
