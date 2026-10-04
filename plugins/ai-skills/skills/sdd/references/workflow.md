# Fluxo e limites

Use estas regras para manter os artefatos coerentes durante a mudança e continuar o trabalho dentro do escopo autorizado.

Conteúdo: Termos comuns · Artefatos e layout · Numeração · Documentos vivos · IDs novos · Conferir com o `check_spec.py` · Escopo e autorização · Decidir e perguntar · Precedência · Fatos · Premissas e lacunas · Corrigir na origem · Idioma

## Termos comuns

| Termo | Significado |
| --- | --- |
| Capability | Algo que o sistema faz ou oferece, com resultado observável e nome que continua válido quando a solução muda |
| Consumidor | Pessoa, sistema ou código que observa o resultado da capability |
| Mudança não trivial | Alteração de comportamento observável, dados persistidos ou contrato consumido por outro componente |

## Artefatos e layout

- Defina o comportamento antes de implementá-lo: reutilize a spec existente ou registre o contrato que a mudança precisa.
- Comece cada artefato novo pelo modelo correspondente de `<skill-dir>/assets/`: `spec.md`, `plan.md` ou `adr.md`. Para ADRs, preserve o formato existente no consumidor. Os modelos fixam o schema; os campos `{{...}}` indicam o que preencher.
- Preencha os campos necessários e remova as linhas e seções opcionais sem conteúdo. Não entregue arquivos vazios nem instruções do modelo.

Sem convenção do repositório, use este layout, com slugs em inglês e em kebab-case:

```text
docs/specs/
  <capability>/
    spec.md                 spec viva da capability, editada no lugar
    NNNN-<change>.md         plano da mudança
docs/adr/NNNN-<decision>.md
```

Reúna a spec e os planos na pasta da capability. Mantenha ADRs fora dessas pastas, pois suas decisões podem alcançar outras capabilities. Preserve outra organização estabelecida pelo consumidor.

Um pedido de cópia para entrega não muda a localização dos artefatos originais. Salve-os no layout do projeto antes de copiar.

Trate PRDs e designs existentes como fontes de comportamento e de decisões técnicas. Não os converta nem os remova sem pedido.

Na implementação por esta skill, mantenha um plano em arquivo para preservar checks e evidências entre sessões. Ajuste o tamanho ao risco: uma mudança pequena pode precisar apenas do cabeçalho e de Checks.

## Numeração

- `NNNN` tem quatro dígitos, começa em `0001` e é o número seguinte ao maior da pasta.
- Cada número pertence a um só item e não muda quando ele é revisado.

## Documentos vivos

- A spec descreve o contrato atual. Altere-a no próprio arquivo, sem cópia nem versão paralela: o diff registra a mudança, e o histórico do Git, a autoria e a evolução.
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
- Artefatos ainda sem commit valem como entrada. Registre em Context do plano a versão que a implementação usou.
- Commit e push seguem a autorização do usuário e não liberam etapas.

## Decidir e perguntar

- Decida por conta própria as escolhas técnicas e editoriais reversíveis dentro do escopo.
- Procure os fatos no código e nas fontes antes de perguntar.
- Pergunte as decisões de negócio e as informações que o contexto não resolve, com opções concretas e a sua recomendação.
- Continue o trabalho independente da resposta e construa o artefato sobre premissas e lacunas. Na implementação, deixe pendente a parte que exige uma decisão ainda ausente e informe o impacto na entrega.
- Exceção: quando a resposta decidiria qual capability especificar ou se o pedido faz sentido, pergunte antes de escrever. Uma lacuna dentro da capability não é motivo para parar.
- Corrija o que a sua mudança quebrar e os problemas preexistentes do trecho alterado que tenham o mesmo motivo da mudança. Os demais entram como sugestão no fim, sem alteração.
- Não acrescente complexidade sem necessidade concreta, como uma opção ou abstração sem consumidor.

## Precedência

- O pedido da sessão prevalece sobre as convenções do repositório, e ambos prevalecem sobre os defaults desta skill e do `check_spec.py`.
- Convenção é a regra escrita no `AGENTS.md`, no `AGENTS.override.md` ou em outra instrução aplicável do repositório.
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

- O que ainda não é fato vai para Assumptions ou para Gaps do artefato onde a questão surge.
- A spec recebe as questões de comportamento e de regra de negócio; o plano, as questões da solução.

### Premissa ou lacuna

Classifique pela decisão em jogo, não pelo default que você escolheria. A primeira linha que se aplicar decide:

| Situação | Registro |
| --- | --- |
| Inferência sobre um fato, como o que o código ou o ambiente faz, e não uma decisão | Premissa, mesmo quando a falsidade custa caro; nomeie quem a verifica |
| Decisão sem default defensável | Lacuna |
| Decisão cuja resposta errada custaria dinheiro, dado, conformidade ou um contrato publicado, mesmo que o default pareça seguro | Lacuna |
| Decisão com default reversível e de impacto contido, como um estado vazio, uma ordenação ou a regra mais comum do domínio | Premissa com a escolha, e o trabalho segue |

Motivo: inventar um valor para uma decisão que ninguém tomou só torna a frase aparentemente verificável.

### Comportamento provisório

- Enquanto uma lacuna estiver aberta e o sistema precisar de um comportamento para o caso, escolha o que preserva o estado atual e não move dinheiro nem dados.
- Registre esse comportamento como premissa `Confirmed? n` que cita a lacuna, e escreva o requisito com ele. O requisito muda quando a lacuna for resolvida.
- Sem comportamento provisório seguro, o requisito só é escrito quando a lacuna for resolvida.
- O corpo do artefato afirma só o que está decidido ou o comportamento provisório de uma premissa.

### Formato da premissa

Cada premissa é um item de lista num só parágrafo, com os rótulos do schema:

```markdown
- **<premissa>.** <origem ou evidência>. Choice: <escolha feita, quando é um default>. If false: <consequência>. Verified by: <quem verifica e como, quando conhecido>. Confirmed? n
```

- `Choice:` aparece quando a premissa é um default; `Verified by:`, quando quem verifica é conhecido, inclusive como papel, como "dono do backend".
- `If false:` e `Confirmed?` são obrigatórios.
- `Confirmed? n` marca o default que ninguém confirmou. Sem esse campo, um default silencioso parece decisão tomada.
- `Confirmed? y (<quem>, <AAAA-MM-DD>)` marca a premissa que o usuário decidiu, inclusive ao delegar a escolha. Nunca marque `y` pela sua própria confiança.
- Agrupe numa premissa só os defaults que o usuário aceitaria ou recusaria juntos, como os estados de uma tela. Decisões que ele pode responder de forma diferente ficam em premissas separadas.
- Ordene as premissas pelo impacto de estarem erradas: primeiro a que inviabilizaria a mudança, depois as que custariam dinheiro, dado ou conformidade, depois as demais.
- Uma premissa sobre um fato não vira fato por ter sido aceita. Ela sai da seção quando for verificada, e o corpo passa a afirmá-la com a origem.
- Para citar uma premissa em outra seção, use o texto em negrito dela. Em outro artefato, acrescente o nome do artefato, como "da spec".

### Formato da lacuna

- Registre as lacunas numa tabela Gap, Affects, Owner: o que falta, os IDs ou o comportamento que ficam indefinidos e quem decide.
- Use `?` em Owner quando ninguém for conhecido.
- Para citar uma lacuna em outra seção, use o texto da coluna Gap dela.
- Quando regras, fontes ou paráfrases se contradisserem, ou quando uma correção depender de decisão de negócio, registre a lacuna com os IDs afetados e conclua o restante. Não escolha uma das versões em silêncio.

## Corrigir na origem

- Corrija a inconsistência onde ela nasce: comportamento e regra de negócio na spec; decisão de solução no plano. Depois atualize os consumidores afetados.
- Uma mudança de comportamento encontrada na verificação segue o mesmo caminho. Ela não sobrevive apenas como observação de revisão.
- Não altere o contrato para fazer um teste passar.
- Não refaça todo o fluxo por causa de um defeito local.

## Idioma

- A prosa de um artefato novo segue o idioma fixado pelo pedido ou pela convenção do repositório.
- Sem essa definição, use o idioma em que o usuário escreveu o pedido. O idioma do código, dos identificadores e da documentação técnica não muda essa escolha.
- O título do artefato e os nomes de exibição, como a coluna State de uma tabela de estados, seguem o idioma da prosa. Slugs de arquivo ficam em inglês.
- Ao editar um artefato existente, preserve o idioma e os títulos dele e não o traduza sem pedido.
- Títulos de seção, rótulos do cabeçalho, colunas de tabela, rótulos de campo e dimensões formam o schema e ficam em inglês, com os nomes das referências, em qualquer idioma de prosa. Leitores e o `check_spec.py` localizam as partes pelo nome, e um schema único dispensa tradução.
- Não traduza nomes de APIs, tipos, paths e identificadores, nem termos canônicos como capability, EARS, NFR, trade-off e gate.
- Outros termos técnicos estabelecidos podem ficar em inglês quando a tradução perder precisão. A permissão vale para termos, não para expressões: em vez de escrever `works as expected` no meio da prosa, descreva o resultado.
