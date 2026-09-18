# Entrada e pesquisa

Antes de escrever, extraia seis informações do material disponível: problema, evidência, usuário, direção da solução, métricas e restrições. Registre de onde vieram e diferencie fatos, inferências (`[ASSUMPTION]`) e decisões pendentes (`[GAP]`).

## Recorte do pedido

| Situação | Ação |
| --- | --- |
| Domínio amplo ou várias iniciativas | Proponha um recorte com resultado identificável. Se a escolha mudar materialmente o escopo, peça a decisão e avance nas partes independentes |
| Pedido descrito como tela, microserviço ou CRUD | Identifique o problema do usuário e a decisão de negócio atendida. Preserve uma interface explicitamente escolhida como parte do produto |

Não transforme a reformulação do problema em recusa de um produto que o usuário já definiu. Uma tela pode ser parte do escopo; seu valor precisa estar explicado.

## Informação suficiente

Com usuário identificado e problema ou direção da solução, escreva e refine o PRD. Com contexto parcial, conclua o que for possível e marque as lacunas materiais. Com apenas um nome ou ideia genérica, reúna as perguntas indispensáveis: problema real, usuário e resultado esperado.

Não repita perguntas já respondidas no material. Pergunte quando a resposta mudar uma decisão indispensável; escolhas editoriais e técnicas reversíveis dentro do escopo não exigem confirmação. Se o usuário pedir para seguir sem descoberta, produza a parte sustentada pelo contexto, explicite `[GAP]` e não invente usuário, métrica ou regra.

## Material de descoberta

Documentos, atas, apresentações, código e PRDs antigos podem fornecer evidência. Avalie a autoridade de cada afirmação: decisão registrada, observação e sugestão têm pesos diferentes. Uma inferência leva `[ASSUMPTION]` e a origem, com página ou seção quando disponível. Fontes conflitantes geram uma lacuna de conciliação; não escolha uma silenciosamente.

Um PRD antigo pode ser o documento a atualizar, a base de um incremento ou uma referência de estilo. Determine a função pelo pedido e pelo conteúdo; esclareça apenas se a ambiguidade afetar o resultado. Sintetize o material em vez de apenas trocar sua formatação. Compare trechos com a fonte quando houver suspeita de cópia ou perda de sentido.

## Pesquisa

Verifique fontes primárias ao introduzir ou atualizar benchmarks, comportamento de usuários, normas e fatos externos que o material não sustenta. Registre link, escopo consultado e data real da consulta. Preserve fontes e limitações; em uma tradução ou revisão editorial, preserve também datas históricas e não afirme ter consultado novamente uma fonte.

Se a fonte não estiver acessível, identifique a afirmação ainda não verificada e continue o trabalho independente. Não preencha a lacuna com um fato lembrado ou uma citação inventada.

Em assuntos regulados, confira o texto vigente antes de alterar uma interpretação normativa e registre o efeito nos requisitos. Distinga o que a norma diz, a interpretação adotada e a regra do produto. Fonte terminológica não é base regulatória; interpretação do modelo não comprova conformidade. Registre pendências como `[GAP]`.
