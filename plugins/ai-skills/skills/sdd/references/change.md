# Alterar um artefato existente

Altere e revise specs, planos e ADRs preservando a identidade dos requisitos e os documentos que dependem deles.

## Antes de alterar

- Antes de alterar ou retirar um requisito ou cenário, procure seu ID ou nome nas specs, nos planos e nos testes. Use `rg -n` ou a busca do projeto, incluindo arquivos novos ainda sem commit.

## IDs de requisito

- Ao ajustar o mesmo comportamento, preserve o ID.
- Ao substituir o conceito, retire o ID e crie outro.
- Ao dividir um requisito, o ID fica com a parte que mantém o conceito do enunciado original, e as demais partes recebem IDs novos.
- Um ID retirado sai do arquivo. As specs e os planos em andamento que o citavam passam a citar o substituto ou deixam de citá-lo; os planos concluídos ficam como estão.
- O documento não guarda lista de IDs retirados: o histórico do Git registra o que cada ID significava.
- Um ID retirado não volta a ser usado, e os demais não são renumerados para fechar buracos na sequência.

## Número repetido entre branches

- Quando branches paralelos chegarem ao mesmo número, mantenha o do item que já estava na branch de destino, dê ao outro o número seguinte ao maior da pasta e atualize quem o cita.

## Revisar um artefato

Numa revisão de spec, plano ou ADR, com profundidade proporcional à mudança, confira:

- Caminhos, links e IDs resolvem para as fontes corretas; a numeração não colide; IDs retirados não voltam.
- Idioma, títulos e formato existentes foram preservados, e cada seção tem conteúdo útil.
- Nenhum placeholder finge que uma decisão foi tomada, e nenhum exemplo aparece como evidência executada.
- Diagramas têm estrutura coerente, e o relatório diferencia inspeção textual de renderização.
