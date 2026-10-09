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
