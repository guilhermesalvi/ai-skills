# Produzir e revisar o PRD

Depois de criar ou alterar um PRD, execute a verificação de estrutura, corrija as falhas que a mudança introduziu e revise o conteúdo antes de entregar.

Uma correção localizada não exige regenerar o PRD inteiro. Revise as seções dependentes quando a mudança afetar regras, exemplos, métricas, estados ou decisões; amplie a leitura pelo impacto, não pela quantidade de seções tocadas.

## Verificação de estrutura

Execute o verificador a partir da raiz do projeto consumidor:

```bash
python "<skill-dir>/scripts/check_prd.py" docs/prd
```

`<skill-dir>` é o caminho absoluto da pasta que contém o `SKILL.md` carregado, não uma variável de ambiente fornecida pela ferramenta. `docs/prd` é o default; use a pasta que a convenção do repositório fixar, relativa à raiz do projeto.

O script lê apenas os arquivos `NNNN-*.md` da pasta, então instruções como `CLAUDE.md` podem conviver ali. Ele confere numeração, cabeçalhos, prefixos, IDs e citações, links locais, seções básicas e integridade textual dos diagramas. Ele não comprova semântica, norma nem renderização; consulte a implementação para o alcance exato.

| Saída | Significado |
| --- | --- |
| `0` | Nenhum achado |
| `1` | Há achados |
| `2` | Erro de entrada |

Corrija os achados e execute de novo. Se um achado corresponder a um formato autorizado pela precedência da skill, preserve o formato e informe a limitação: não altere o produto para satisfazer uma expressão regular. Se Python não estiver disponível, faça a conferência manual e declare que o script não foi executado.

## Revisão de conteúdo

Releia o PRD contra as seções Capacidade de produto e Uma regra e seus usos de [requisitos e seções](writing.md): os requisitos descrevem comportamento observável e cada regra tem uma definição principal.

Confira se fórmulas, limites, exemplos, estados e eventos coincidem entre as seções e entre os PRDs que citam os mesmos IDs.

## Entrega

Informe na resposta o caminho do PRD, o resultado da revisão, as decisões ainda necessárias e as verificações não realizadas. Cite os IDs e os consumidores atingidos por mudanças normativas.
