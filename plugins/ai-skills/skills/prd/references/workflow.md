# Produzir e revisar o PRD

Depois de criar ou alterar um PRD, confira a estrutura, corrija as falhas que a mudança introduziu e revise o conteúdo antes de entregar.

Uma correção localizada não exige regenerar o PRD inteiro. Revise as seções dependentes quando a mudança afetar regras, exemplos, métricas, estados ou decisões; amplie a leitura pelo impacto, não pela quantidade de seções tocadas.

## Conferência de estrutura

Confira nos PRDs tocados e nos que citam seus IDs:

- Cada número de arquivo pertence a um só documento, e cada prefixo, a um só PRD.
- Cada ID é definido uma única vez, e toda citação resolve para uma definição existente. Use `git grep -n` para procurar os IDs.
- Requisitos funcionais têm prioridade MoSCoW; NFRs não têm.
- As seções base existem, nenhuma seção está vazia, e só Referências vem depois de Ponto mais frágil.
- Cada trade-off declarado tem custo e motivo.
- Links locais apontam para arquivos existentes, e cada diagrama Mermaid declara um tipo suportado.

## Revisão de conteúdo

Releia o PRD contra as seções Capacidade de produto e Uma regra e seus usos de [requisitos e seções](writing.md): os requisitos descrevem comportamento observável e cada regra tem uma definição principal.

Confira se fórmulas, limites, exemplos, estados e eventos coincidem entre as seções e entre os PRDs que citam os mesmos IDs.

## Entrega

Informe na resposta o caminho do PRD, o resultado da revisão, as decisões ainda necessárias e as verificações não realizadas. Cite os IDs e os consumidores atingidos por mudanças normativas.
