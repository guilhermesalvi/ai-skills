# Produzir e revisar o PRD

## Fluxo

Depois de escrever ou revisar o documento, execute a verificação de estrutura, corrija as falhas introduzidas pela mudança e revise o conteúdo antes de entregar.

Uma correção localizada não exige regenerar o PRD inteiro. Revise as seções dependentes quando a mudança afetar regras, exemplos, métricas, estados ou decisões. Amplie a leitura pelo impacto, não pela quantidade de seções tocadas.

## Verificação de estrutura

Execute o comando da verificação de estrutura sempre que criar ou alterar PRDs. O script lê só os arquivos `NNNN-*.md` da pasta, então instruções como `CLAUDE.md` podem ficar nela. Ele confere numeração, cabeçalhos, prefixos, IDs e citações, links locais, seções básicas e integridade textual dos diagramas; não comprova semântica, norma nem renderização. Saída 0 indica ausência de achados; 1, achados; 2, erro de entrada. Consulte a implementação para o alcance exato.

Corrija os achados e execute de novo. Se um achado corresponder a um formato autorizado conforme a precedência da skill, preserve o formato e informe a limitação; não altere o produto para satisfazer uma expressão regular. Se Python não estiver disponível, faça a conferência manual e declare que o script não foi executado.

## Revisão de conteúdo

Releia o PRD contra as seções Capacidade de produto e Uma regra e seus usos de [redação](writing.md): os requisitos descrevem comportamento observável e cada regra tem uma definição principal. Confira se fórmulas, limites, exemplos, estados e eventos coincidem entre as seções e entre os PRDs que citam os mesmos IDs. Se uma correção depender de decisão de negócio, registre um `[GAP]` e conclua o restante.

## Entrega

Informe na resposta o caminho do PRD, o resultado da revisão, decisões ainda necessárias e verificações não realizadas. Cite os IDs e consumidores atingidos por mudanças normativas.
