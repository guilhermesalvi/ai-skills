# Fluxo e limites

Use estas regras para manter os artefatos coerentes durante a mudança e continuar o trabalho dentro do escopo autorizado.

Conteúdo: Termos comuns · Artefatos e layout · Numeração · Documentos vivos · IDs novos · Conferir com o `check_spec.py` · Escopo e autorização · Decidir e perguntar · Precedência · Fatos · Premissas e lacunas · Corrigir na origem · Idioma

## Termos comuns

| Termo | Significado |
| --- | --- |
| Comportamento completo | Recorte com gatilho identificável e resultado observável para um consumidor, incluindo as regras e alternativas necessárias para chegar a esse resultado |
| Capability | Agrupamento de comportamentos relacionados, usado quando ajuda a organizar o domínio |
| Consumidor | Pessoa, sistema ou código que observa o resultado do comportamento |
| Mudança não trivial | Alteração de comportamento observável, dados persistidos ou contrato consumido por outro componente |
| Revisar | Conferir um artefato ou uma implementação e relatar achados. Alterar o conteúdo exige pedido de alteração ou de correção |

## Artefatos e layout

- Defina o comportamento antes de implementá-lo: reutilize a spec existente ou registre o contrato que a mudança precisa.
- Comece cada artefato novo pelo modelo correspondente de `<skill-dir>/assets/`: `spec.md`, `plan.md` ou `adr.md`. Para ADRs, preserve o formato existente no consumidor. Os modelos fixam o schema; os campos `{{...}}` indicam o que preencher.
- Preencha os campos necessários e remova as linhas e seções opcionais sem conteúdo. Não entregue arquivos vazios nem instruções do modelo.

Sem convenção do repositório, use este layout, com slugs em inglês e em kebab-case:

```text
docs/specs/
  <behavior>/
    spec.md                 contrato vivo do comportamento, editado no lugar
    NNNN-<change>.md         plano da mudança
docs/adr/NNNN-<decision>.md
```

Reúna a spec e os planos na pasta do comportamento. Quando um agrupamento facilitar a navegação, use `docs/specs/<capability>/<behavior>/` com os mesmos arquivos. Mantenha ADRs fora dessas pastas, pois suas decisões podem alcançar múltiplos comportamentos. Preserve outra organização estabelecida pelo consumidor; não reorganize specs existentes apenas para adotar este default.

Um pedido de cópia para entrega não muda a localização dos artefatos originais. Salve-os no layout do projeto antes de copiar.

Trate PRDs e designs existentes como fontes de comportamento e de decisões técnicas. Não os converta nem os remova sem pedido.

Na implementação por esta skill, mantenha um plano em arquivo para preservar checks e evidências entre sessões. Ajuste o tamanho ao risco: uma mudança pequena pode precisar apenas do cabeçalho e de Checks.

## Numeração

- Numere os planos na pasta da spec e os ADRs na pasta de ADRs. Cada pasta tem sua própria sequência: `NNNN` tem quatro dígitos; numa pasta sem itens numerados, use `0001`; nos demais casos, use o número seguinte ao maior presente naquela pasta.
- Dentro da mesma pasta, cada número pertence a um só item e não muda quando ele é alterado.

## Documentos vivos

- A spec descreve o contrato que a implementação deve cumprir. Altere-a no próprio arquivo, sem cópia nem versão paralela: o diff registra a mudança, e o histórico do Git, a autoria e a evolução.
- O andamento da implementação pertence ao plano e à entrega, nunca à spec.
- Ficam fora da spec, porque não descrevem o contrato:
  - instruções dirigidas ao agente ou a quem edita o documento;
  - histórico de revisões;
  - campos de aprovação e status do documento, como rascunho, validado ou aprovado;
  - resultado das verificações e da revisão, que a entrega informa na resposta;
  - notas sobre a ferramenta que gerou ou editou o texto;
  - exemplos que ilustram o método de escrita. Exemplos que especificam o comportamento, como tabelas de cálculo e cenários de aceitação, continuam no documento.
- Um plano concluído, já em commit e com todos os checks marcados, é o registro histórico da mudança. Não o reescreva para acompanhar a spec.

## IDs novos

- Um ID novo recebe o número seguinte ao maior já usado com o mesmo prefixo.
- Antes de usar um ID novo, confira com `git log -S "<ID>"` que ele nunca existiu, porque o maior número pode ter sido retirado.
- Para um prefixo novo, uma única conferência com `git log -S "<PREFIX>-"` substitui a de cada ID.
- Sem o histórico completo, como num clone raso ou fora de um repositório Git, informe na entrega que a conferência não foi feita.

## Conferir com o `check_spec.py`

Depois de criar ou alterar uma spec ou um plano, execute a partir da raiz do projeto consumidor:

```bash
python "<skill-dir>/scripts/check_spec.py" docs/specs
```

- `docs/specs` é o default. Use a pasta que a convenção do repositório fixar, relativa à raiz do projeto.
- Corrija os achados e execute de novo até a saída `0`.
- Interprete a saída `0` como conferência de forma, não como aprovação do comportamento. Revise o conteúdo das premissas, lacunas e requisitos.
- A saída `1` traz achados; a `2`, um erro de entrada, como uma pasta sem specs.
- Sem Python, aplique à mão as conferências que a docstring do script lista e declare na entrega que o script não foi executado.

## Escopo e autorização

| Pedido | Trabalho autorizado pela skill |
| --- | --- |
| Spec ou plano | Produza e confira o artefato pedido |
| Implementação | Crie a spec e o plano que faltarem, implemente, verifique e corrija dentro do escopo, sem aprovações intermediárias |
| Revisão | Confira o artefato ou a implementação e entregue os achados; aplique correções quando o pedido as autorizar |

- Num pedido de implementação, acrescente requisitos para as dimensões técnicas que a mudança expõe. Não mude o resultado observável de um requisito existente, porque essa decisão pertence ao usuário.
- Uma regra de negócio ausente segue Premissas e lacunas: nunca é decidida em silêncio.
- Artefatos ainda sem commit valem como entrada. Registre em Context do plano o estado dos artefatos usado na implementação, incluindo as alterações locais pertinentes.
- Commit e push seguem a autorização do usuário e não liberam etapas.

## Decidir e perguntar

- Decida por conta própria as escolhas técnicas e editoriais reversíveis dentro do escopo.
- Procure os fatos no código e nas fontes antes de perguntar.
- Pergunte as decisões de negócio e as informações que o contexto não resolve, com opções concretas e a sua recomendação. Reúna essas perguntas na resposta final, conforme [entrega](deliver.md#resposta), sem interromper o trabalho para fazê-las.
- Construa o artefato sobre premissas e lacunas enquanto a resposta não vem. Na implementação, deixe pendente a parte que exige uma decisão ainda ausente e informe o impacto na entrega.
- Exceção: quando a resposta decidiria qual comportamento especificar ou se o pedido faz sentido, pergunte antes de escrever. Uma lacuna dentro do comportamento não é motivo para parar o trabalho independente.
- Corrija o que a sua mudança quebrar e os problemas preexistentes do trecho alterado que tenham o mesmo motivo da mudança. Os demais entram como sugestão no fim, sem alteração.
- Não acrescente complexidade sem necessidade concreta, como uma opção ou abstração sem consumidor.

## Precedência

- O pedido da sessão prevalece sobre as convenções do repositório, e ambos prevalecem sobre os defaults desta skill e do `check_spec.py`.
- Convenção é a regra escrita no `CLAUDE.md`, no `CLAUDE.local.md`, no `AGENTS.md` ou em outra instrução aplicável do repositório.
- Um padrão apenas observado em arquivos existentes não obriga, mas preserve-o ao editar esses arquivos.
- Trate um ADR vigente como restrição técnica. Quando o pedido autorizar sua substituição, registre-a conforme [ADR](adr.md). Quando o conflito não estiver resolvido, registre a lacuna e continue o trabalho independente; não use o ADR para anular uma escolha explícita do usuário.
- Se uma regra local parecer impedir o trabalho, informe o arquivo, a regra e a ação afetada.

## Fatos

- Um fato aponta para a origem: decisão do usuário, regra formalizada, documento de produto, código, documentação, observação ou fonte pertinente.
- Verifique em fonte primária o fato externo que o material não sustenta, como API, versão de pacote, norma ou limite de provedor.
- Registre link, escopo e data real da consulta em References do artefato cuja afirmação a fonte sustenta.
- Sem acesso à fonte, declare a afirmação como não verificada. Não invente APIs, ferramentas nem comportamento.

## Premissas e lacunas

### Onde registrar

- Nas specs e nos planos, registre em Assumptions ou Gaps o que ainda não é fato ou decisão tomada.
- A spec recebe as questões de comportamento e de regra de negócio; o plano, as questões da solução.
- Num ADR, registre inferências e informações ausentes conforme [ADR](adr.md), preservando o schema desse artefato.

### Premissa ou lacuna

Classifique pela decisão em jogo, não pelo default que você escolheria. A primeira linha que se aplicar decide:

| Situação | Registro |
| --- | --- |
| Inferência sobre um fato, como o que o código ou o ambiente faz, e não uma decisão | Premissa, mesmo quando a falsidade custa caro; nomeie quem a verifica |
| Decisão cuja resposta errada custaria dinheiro, dado, conformidade ou um contrato publicado, mesmo que o default pareça seguro | Lacuna |
| Decisão com default reversível e de impacto contido, como um estado vazio, uma ordenação ou a regra mais comum do domínio | Premissa com a escolha, e o trabalho segue |
| Qualquer outra decisão, como uma sem default defensável ou com efeito que não se desfaz | Lacuna |

Motivo: inventar um valor para uma decisão que ninguém tomou só torna a frase aparentemente verificável.

### Comportamento provisório

- Enquanto uma lacuna estiver aberta e o sistema precisar de um comportamento para o caso, escolha o que preserva o estado atual e não move dinheiro nem dados.
- Registre esse comportamento como escolha provisória em Assumptions que cita a lacuna, e escreva o requisito com ele. O requisito muda quando a lacuna for resolvida.
- Sem comportamento provisório seguro, o requisito só é escrito quando a lacuna for resolvida.
- O corpo do artefato afirma só o que está decidido ou o comportamento provisório de uma premissa.

### Formato da premissa

Mantenha em Assumptions apenas fatos ainda não verificados e escolhas provisórias. Escreva cada premissa como um item de lista num só parágrafo. Comece por um título curto em negrito, que nomeia o assunto e serve para citá-la; depois, em prosa, escreva a afirmação, o fundamento, a escolha provisória quando houver e a consequência de estar errada. Nomeie quem verifica e como, quando conhecido, inclusive como papel, como "dono do backend". Use prosa natural, sem campos de status ou rótulos dentro do parágrafo.

Exemplo de inferência ainda aberta:

```markdown
- **Serialização pelo chamador.** O chamador serializa as operações sobre o mesmo pedido: o módulo altera o pedido em memória e não expõe uma trava, e o dono do backend ainda precisa verificar essa serialização. Se ela não existir, um pagamento concorrente pode cobrar um pedido cancelado.
```

- Agrupe numa premissa só os defaults que o usuário aceitaria ou recusaria juntos, como os estados de uma tela. Decisões que ele pode responder de forma diferente ficam em premissas separadas.
- Ordene as premissas pelo impacto de estarem erradas: primeiro a que inviabilizaria a mudança, depois as que custariam dinheiro, dado ou conformidade, depois as demais.
- Para citar uma premissa em outra seção, use o título dela. Em outro artefato, acrescente o nome do artefato, como "da spec". Preserve o título ao editar a premissa, para não romper as citações.

### Quando a premissa for resolvida

Retire a premissa de Assumptions quando houver evidência ou decisão suficiente e registre o resultado no lugar correspondente:

| Resolução | Destino e origem |
| --- | --- |
| Fato verificado | Context ou a seção que usa o fato, com a evidência que o comprova |
| Escolha decidida pelo usuário, inclusive por delegação | Requirements na spec ou Technical Decisions no plano, com a origem da decisão; registre quem decidiu e a data quando conhecidos |

- Aceitar uma inferência não comprova um fato. Mantenha a premissa aberta até verificar a afirmação.
- Atualize os requisitos e as citações que dependiam da premissa. Se ela atendia uma lacuna, resolva também o registro em Gaps. Apague Assumptions quando a seção ficar vazia.

### Formato da lacuna

- Registre as lacunas numa tabela Gap, Affects, Owner: o que falta, os IDs ou o comportamento que ficam indefinidos e quem decide.
- Use `?` em Owner quando ninguém for conhecido.
- Para citar uma lacuna em outra seção, use o texto da coluna Gap dela e preserve esse texto ao editar a lacuna.
- Quando regras, fontes ou paráfrases se contradisserem, ou quando uma correção depender de decisão de negócio, registre a lacuna com os IDs afetados e conclua o restante. Não escolha uma das versões em silêncio.

## Corrigir na origem

- Corrija a inconsistência onde ela nasce: comportamento e regra de negócio na spec; decisão de solução no plano. Depois atualize os consumidores afetados.
- Uma mudança de comportamento encontrada na verificação segue o mesmo caminho. Ela não sobrevive apenas como observação de revisão.
- Não altere o contrato para fazer um teste passar.
- Não refaça todo o fluxo por causa de um defeito local.

## Idioma

- A prosa de um artefato novo segue o idioma fixado pelo pedido ou pela convenção do repositório.
- Sem essa definição, use o idioma em que o usuário escreveu o pedido. O idioma do código, dos identificadores e da documentação técnica não muda essa escolha.
- O título do artefato e os valores de exibição, como os nomes listados na coluna State de uma tabela de estados, seguem o idioma da prosa. O cabeçalho da coluna e os slugs de arquivo ficam em inglês.
- Ao editar um artefato existente, preserve o idioma e os títulos dele e não o traduza sem pedido.
- Títulos de seção, rótulos do cabeçalho, colunas de tabela, rótulos de campo e dimensões formam o schema e ficam em inglês, com os nomes das referências, em qualquer idioma de prosa. Leitores e o `check_spec.py` localizam as partes pelo nome, e um schema único dispensa tradução.
- Não traduza nomes de APIs, tipos, paths e identificadores, nem termos canônicos como capability, EARS, NFR, trade-off e gate.
- Outros termos técnicos estabelecidos podem ficar em inglês quando a tradução perder precisão. A permissão vale para termos, não para expressões: em vez de escrever `works as expected` no meio da prosa, descreva o resultado.
