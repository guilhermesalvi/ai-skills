# Fluxo e limites

## Dimensionar os artefatos

Defina o comportamento antes de implementá-lo. Reutilize uma spec existente ou registre o contrato necessário para a mudança; não crie arquivos vazios.

Sem convenção do repositório, use este layout, com slugs em inglês e em kebab-case. A pasta de uma capability reúne a spec e os planos das mudanças dela:

```text
docs/specs/
  <capability>/
    spec.md                 spec viva da capability, editada no lugar
    NNNN-<change>.md        plano da mudança
docs/adr/NNNN-<decision>.md
```

O ADR fica fora das pastas de capability porque registra uma decisão que vale para outras capabilities.

`NNNN` tem quatro dígitos, começa em `0001` e é o número seguinte ao maior da pasta. Cada número pertence a um só item e não muda quando ele é revisado. Se branches paralelos chegarem ao mesmo número, mantenha o do item que já estava na branch de destino, dê ao outro o número seguinte ao maior da pasta e atualize quem o cita. Preserve outra organização já estabelecida no repositório. Os planos ficam na pasta da capability, não numa pasta de planos independente.

Num repositório que já tem PRD ou design, trate o PRD como material de origem da spec e o design como as decisões técnicas do plano da mudança. Não os converta nem os remova sem pedido.

Toda implementação tem um plano em arquivo, mesmo a pequena: é nele que os checks sobrevivem à sessão, são marcados e chegam ao verificador. O tamanho do plano acompanha o risco da mudança, não a quantidade de arquivos ou de exemplos encontrados; uma mudança pequena pode ter só Checks.

## Documentos vivos

A spec descreve o contrato atual. Altere-a no próprio arquivo, sem cópia ou versão paralela: o diff registra a mudança, e o histórico do Git, a autoria e a evolução.

O andamento da implementação pertence ao plano e à entrega; não o registre na spec. Ficam fora dela, porque não descrevem o contrato:

- instruções dirigidas ao agente ou a quem edita o documento;
- histórico de revisões;
- campos de aprovação e status do documento, como rascunho, validado ou aprovado;
- resultado das verificações e da revisão, que a entrega informa na resposta;
- notas sobre a ferramenta que gerou ou editou o texto;
- exemplos que ilustram o método de escrita em vez do comportamento. Exemplos que especificam o comportamento, como tabelas de cálculo e cenários de aceitação, continuam no documento.

## IDs de requisito

Ao ajustar o mesmo comportamento, preserve o ID dele; ao substituir o conceito, retire o ID e crie outro.

Antes de alterar ou retirar um requisito ou um cenário de aceitação, procure o ID ou o nome do cenário com `git grep -n` para encontrar as specs, os planos e os testes que dependem dele. Um ID retirado sai do arquivo, e quem o citava passa a citar o substituto ou deixa de citá-lo. O documento não guarda lista de retirados: o histórico do Git registra o que o ID significava.

Um ID novo recebe o número seguinte ao maior já usado com o mesmo prefixo. Como o maior número pode ter sido retirado, confira com `git log -S "<ID>"` que o candidato nunca existiu. Um prefixo novo dispensa a conferência; sem o histórico completo, como num clone raso ou fora de um repositório Git, informe na entrega que ela não foi feita. Um ID retirado não volta a ser usado, e os demais não são renumerados para fechar buracos na sequência.

Depois de criar ou alterar uma spec ou um plano, execute o verificador a partir da raiz do projeto consumidor:

```bash
python "<skill-dir>/scripts/check_spec.py" docs/specs
```

`<skill-dir>` é o caminho absoluto da pasta que contém o `SKILL.md` carregado, não uma variável de ambiente fornecida pela ferramenta. `docs/specs` é o default; use a pasta que a convenção do repositório fixar, relativa à raiz do projeto.

O script lê o `spec.md` e os planos `NNNN-<change>.md` de cada pasta de capability. Ele confere:

- a definição única de cada ID, um prefixo por spec, exclusivo entre elas e igual ao Requirement Prefix do cabeçalho, citações sem definição, links locais e cercas de código abertas;
- as seções base, seção sem conteúdo, premissa sem `Confirmed?` e célula vazia nas tabelas de Gaps, Observable Decisions, Trade-offs e Technical Decisions;
- no plano, check que não é checkbox ou não termina com a prova num trecho de código.

Um artefato cujos títulos não seguem o schema recebe só os checks de IDs e links, e a saída o lista como não conferido. Nos demais arquivos Markdown das pastas de capability, o script confere só as citações. A saída é `0` sem achados, `1` com achados e `2` para erro de entrada. Corrija os achados e execute de novo; sem Python, confira esses pontos à mão e declare que o script não foi executado.

## Escopo e autorização

O pedido define as etapas autorizadas:

- **Pedido de spec ou plano.** Termina no artefato.
- **Pedido de implementação.** Autoriza a spec que faltar, o planejamento necessário, a execução, a verificação e as correções dentro do escopo, sem aprovações intermediárias. Autoriza acrescentar requisitos para as dimensões técnicas que a mudança expõe, mas não mudar o resultado observável de um requisito existente, porque essa decisão pertence ao usuário. Uma regra de negócio ausente segue a seção Fatos, premissas e lacunas: nunca é decidida em silêncio.

Artefatos ainda sem commit valem como entrada; registre qual versão a implementação usou. Commit e push seguem a autorização do usuário e não liberam etapas.

Decida por conta própria as escolhas técnicas e editoriais reversíveis dentro do escopo. Procure os fatos no código e nas fontes; pergunte as decisões de negócio e as informações que o contexto não resolve, com opções concretas e a sua recomendação, e continue o trabalho independente enquanto espera.

Corrija o que a sua mudança quebrar e os problemas preexistentes do trecho alterado que tenham o mesmo motivo da mudança. Os demais entram como sugestão no fim, sem alteração. Não acrescente complexidade sem necessidade concreta, como uma opção ou abstração sem consumidor.

## Precedência

O pedido da sessão prevalece sobre as convenções do repositório, e ambos prevalecem sobre os defaults desta skill e do verificador. Convenção é a regra escrita no `CLAUDE.md` ou em outra instrução do repositório; um padrão apenas observado em arquivos existentes não obriga, mas preserve-o ao editá-los.

Se uma regra local parecer impedir o trabalho, informe o arquivo, a regra e a ação afetada.

## Fatos, premissas e lacunas

Um fato aponta para sua origem: decisão do usuário, regra formalizada, documento de produto, código, documentação, observação ou fonte pertinente. Verifique em fonte primária o fato externo que o material não sustenta, como API, versão de pacote, norma ou limite de provedor, e registre link, escopo e data real da consulta em References do artefato cuja afirmação a fonte sustenta. Sem acesso à fonte, declare a afirmação como não verificada: não invente APIs, ferramentas ou comportamento.

O que ainda não é fato vai para Assumptions ou para Gaps do artefato onde a questão surge: a spec, para comportamento e regras de negócio; o plano, para a solução.

Uma decisão que ninguém tomou vira premissa ou lacuna conforme exista um default defensável. Com default reversível e de impacto contido, como um estado vazio, uma ordenação ou a regra mais comum do domínio, registre a premissa com a escolha e siga. Sem default defensável, ou quando o erro custaria dinheiro, dado, conformidade ou um contrato publicado, a decisão é lacuna: inventar um valor só torna a frase aparentemente verificável.

Uma premissa é uma inferência ou um default que o trabalho usa. Registre cada premissa como um item de lista, num só parágrafo: a premissa em negrito, a origem ou a evidência que a motivou, a escolha feita quando for um default, a consequência se ela for falsa e, quando conhecidos, quem a verifica e como. O item termina com `Confirmed? y` quando o usuário decidiu, inclusive ao delegar a escolha, ou `Confirmed? n` para o default que ninguém viu. Sem esse campo, um default silencioso parece decisão tomada. Defaults do mesmo tipo, como os estados de uma tela ou as faixas de validação de um formulário, formam uma premissa só.

Comece pela premissa cuja falsidade inviabilizaria a mudança. Uma premissa sobre um fato não vira fato por ter sido aceita: ela sai da seção quando for verificada, e o corpo passa a afirmá-la com a origem.

Uma lacuna é uma informação ou decisão ausente. Registre as lacunas numa tabela Gap, Affects, Owner: o que falta, os IDs ou o comportamento que ficam indefinidos e quem decide, ou `?` quando ninguém for conhecido. O corpo do artefato afirma só o que está decidido, e um requisito que depende inteiramente de uma lacuna só é escrito quando ela for resolvida.

Quando regras, fontes ou paráfrases se contradisserem, ou quando uma correção depender de decisão de negócio, registre a lacuna com os IDs afetados e conclua o restante. Não escolha uma das versões em silêncio.

Corrija a inconsistência na origem dela: comportamento e regra de negócio na spec, decisão de solução no plano. Depois atualize os consumidores afetados. Uma mudança de comportamento encontrada na verificação segue o mesmo caminho; ela não sobrevive apenas como observação de revisão.

Não altere o contrato para fazer um teste passar, nem refaça todo o fluxo por causa de um defeito local.

## Revisar um artefato

Numa revisão de spec, plano ou ADR, com profundidade proporcional à mudança, confira também:

- Caminhos, links e IDs resolvem para as fontes corretas; a numeração não colide e IDs retirados não voltam.
- Idioma, títulos e formato existentes foram preservados e cada seção tem conteúdo útil.
- Nenhum placeholder finge que uma decisão foi tomada, e nenhum exemplo aparece como evidência executada.
- Diagramas têm estrutura coerente, e o relatório diferencia inspeção textual de renderização.

## Idioma

A prosa de um artefato novo segue o idioma fixado pelo pedido ou pela convenção do repositório. Sem essa definição, use o do material de origem e, sem material, o idioma em que o pedido foi escrito.

Títulos de seção, rótulos do cabeçalho, colunas de tabela e campos formam o schema dos artefatos e ficam em inglês, com os nomes das referências, em qualquer idioma de prosa: leitores e o verificador localizam as seções pelo nome, e um schema único dispensa tradução. Ao editar um artefato existente com outros títulos, preserve-os e não traduza o documento sem pedido.

Nomes de APIs, tipos, paths e identificadores não se traduzem, nem termos canônicos como capability, EARS, NFR, trade-off e gate. Outros termos técnicos estabelecidos podem ficar em inglês na prosa quando a tradução perder precisão. A permissão vale para termos, não para expressões: em vez de escrever `if false` no meio da prosa, descreva a condição e o seu impacto.
