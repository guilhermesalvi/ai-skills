# PRD

Entregue um PRD que explique o problema, o usuário afetado, o comportamento esperado, os requisitos verificáveis e o custo das decisões tomadas. O PRD é a fonte canônica do contrato de produto de uma capability: propósito, escopo, comportamento e requisitos.

## Escolher a leitura

Leia as referências cujo gatilho o pedido aciona; um pedido pode acionar várias.

| Referência | Quando ler | O que entrega |
| --- | --- | --- |
| [Entrada e pesquisa](prd/intake.md) | Ao criar um PRD, ou ao incorporar material de descoberta ou fato externo | Recorte do pedido, suficiência da informação, peso das fontes e regras de pesquisa |
| [Requisitos e seções](prd/writing.md) | Ao criar um PRD; ao editar, nas regras que a mudança toca | Comportamento observável, capabilities e eventos, forma dos requisitos, diagramas, seções, premissas e lacunas |
| [Convenções](prd/conventions.md) | Ao criar ou editar um PRD | Cabeçalho, IDs e nomes de seção por idioma |
| [Modos](prd/modes.md) | Quando o PRD documenta produto existente, atende outros times ou sistemas (plataforma, infraestrutura, SDK, API) ou é a visão geral 0000 | Ajustes de evidência, seções e estrutura de cada modo |
| [Exemplo](prd/example.md) | Quando a forma de um PRD não estiver clara; leia só o trecho pertinente | PRD de capability e exemplo de edição |

## Produzir e revisar

Depois de criar ou alterar um PRD, execute o verificador, confira a estrutura, corrija as falhas que a mudança introduziu e revise o conteúdo antes de entregar.

Uma correção localizada não exige regenerar o PRD inteiro. Revise as seções dependentes quando a mudança afetar regras, exemplos, métricas, estados ou decisões; amplie a leitura pelo impacto, não pela quantidade de seções tocadas.

### Verificação de IDs e links

Execute o verificador a partir da raiz do projeto consumidor:

```bash
python "<skill-dir>/scripts/check_prd.py" docs/prd
```

`<skill-dir>` é o caminho absoluto da pasta que contém o `SKILL.md` carregado, não uma variável de ambiente fornecida pela ferramenta. `docs/prd` é o default; use a pasta que a convenção do repositório fixar, relativa à raiz do projeto.

O script lê só os arquivos `NNNN-*.md` e ignora títulos e rótulos, então funciona em qualquer idioma. Ele confere numeração, definição única de cada ID, prefixo exclusivo por PRD, prioridade MoSCoW, citações sem definição, links locais e cercas de código abertas. Um requisito conta como definição quando o item de lista começa pelo ID em negrito, como no exemplo de IDs das convenções.

| Saída | Significado |
| --- | --- |
| `0` | Nenhum achado |
| `1` | Há achados |
| `2` | Erro de entrada |

Corrija os achados e execute de novo. Se Python não estiver disponível, confira esses pontos à mão e declare que o script não foi executado.

### Conferência de estrutura

O script não lê a estrutura do documento. Confira nos PRDs tocados:

- As seções base existem, nenhuma seção está vazia, e só Referências vem depois de Ponto mais frágil.
- Cada trade-off declarado tem custo e motivo.
- Cada diagrama Mermaid declara um tipo suportado.

### Revisão de conteúdo

Releia o PRD contra as seções Comportamento observável e Uma regra e seus usos de [requisitos e seções](prd/writing.md): os requisitos descrevem comportamento observável e cada regra tem uma definição principal.

Confira se fórmulas, limites, exemplos, estados e eventos coincidem entre as seções e entre os PRDs que citam os mesmos IDs.

### Entrega

Informe na resposta o caminho do PRD, o resultado da revisão, as decisões ainda necessárias e as verificações não realizadas. Cite os IDs e os consumidores atingidos por mudanças normativas.
