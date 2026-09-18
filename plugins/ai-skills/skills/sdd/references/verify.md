# Verificação

Confronte a implementação com a spec e o design atuais. Informe quais requisitos têm evidência, quais estão sem cobertura e quais ainda não definem um resultado preciso. O relatório normalmente vai na resposta; salve um artefato quando o pedido ou a necessidade de rastreabilidade justificar.

## Escopo e leitura crítica

Compare contra a base da mudança, incluindo arquivos novos autorizados. Use a base registrada antes da primeira alteração ou, com branch própria, `git merge-base HEAD <branch principal>`. O último commit da spec não serve de base, porque uma spec viva acumula mudanças diferentes. Se não for possível recuperar a base, declare a limitação de regressão e verifique o estado atual sem inventar uma origem.

Preserve alterações alheias: a revisão não exige `add`, `stash`, restauração ou troca de checkout. Leia os requisitos e os testes antes de consultar a conclusão do implementador, para reduzir a confirmação automática da própria solução.

Verifique em contexto separado do que implementou sempre que houver subagente disponível e a mudança não for trivial. Dois motivos independentes apontam para isso: quem escreveu o código reaplica o raciocínio que produziu a lacuna, e uma janela já ocupada pela implementação chega à verificação com pior relação entre sinal e ruído. O subagente recebe os caminhos da spec, do design e do plano, a base do diff, os comandos de verificação e o conjunto completo de requisitos em escopo — nunca apenas a última fatia implementada, porque um resultado sobre parte do escopo se lê igual a um resultado sobre o todo.

Sem subagente disponível, verifique mesmo assim e declare no relatório que autor e verificador são o mesmo. Uma limitação declarada vale mais que uma independência presumida.

## Conformidade com a spec

| Requisito | Resultado esperado | Evidência | Situação |
| --- | --- | --- | --- |
| ID em escopo | Estado, valor, erro ou evento definido | `arquivo:linha`, asserção e resultado do check | Coberto, lacuna de cobertura ou requisito impreciso |

A asserção precisa observar o resultado exigido; a existência de um teste qualquer não basta. Antes de declarar ausência, procure o ID e os identificadores de estado, erro ou evento nos testes pertinentes. Um requisito sem evidência fica como lacuna; um requisito sem resultado definido volta à spec.

Cite `arquivo:linha` e reproduza a expressão da asserção que resolve o requisito, não todas as asserções do teste. A expressão é a evidência: quando o valor esperado não é legível ali, porque vem de uma fixture montada em outro arquivo, isso é achado sobre o teste e não pesquisa a fazer.

Para um comportamento retirado, confira a remoção do caminho de código e o ajuste correspondente dos testes. Reorganizar testes pode mudar sua contagem sem reduzir a cobertura; investigue o motivo em vez de tratar toda redução como regressão automática.

Um teste prova a camada em que asserta, não as camadas que atravessa. Um teste ponta a ponta percorre um caminho da tabela de decisão e não falha quando outro ramo está errado, então tratá-lo como prova do código atravessado troca o nível da evidência. Um requisito que cita status HTTP, rota ou formato de resposta e só tem evidência abaixo dessa fronteira é lacuna de nível, por mais asserções que carregue. Quando requisito e evidência ficam em níveis diferentes, ou o requisito se divide ou a evidência ganha uma segunda linha; não deixe o nível escorregar para o que é mais barato de escrever.

## Cobertura dos conjuntos

Um requisito que quantifica sobre um conjunto se satisfaz por frase e se reprova por membro. Dê uma linha a cada conjunto que a mudança precisa cobrir e escreva cada membro como um item próprio, ao lado da evidência que o observa. Um conjunto colapsado em frase não tem célula vazia, então um membro some sem que nada apareça.

| Conjunto e tamanho | Membro e evidência | Sem evidência |
| --- | --- | --- |
| Status do provedor (9) | EXM-04, prova por tabela sobre os 9 | `-` |
| Tipos de evento recebidos (4) | `paused` EXM-05 · `updated` EXM-06 · `deleted` EXM-07 · `trial_end` EXM-08 | `-` |

Uma prova única que percorre o conjunto inteiro vale pela linha, com o tamanho declarado, porque nesse caso a enumeração vive no teste.

Percorra a partir dos conjuntos, não das evidências. Resumir os testes escritos só encontra teste sem lastro; não encontra membro sem teste, que é a omissão que custa. Tire os membros de quem tem autoridade sobre o conjunto: os status de um provedor vêm do provedor e as rotas de um framework vêm do framework, mas um conjunto que o código deveria satisfazer — as telas que um design define, os campos que um contrato declara — tem autoridade fora do código. Recomputar esses a partir da implementação pergunta ao próprio resultado se ele está completo, e a resposta é sempre sim.

A configuração de inicialização também é um conjunto, e seus membros são lugares. Uma suíte monta a própria composição da aplicação, então uma prova só observa a montagem que ela mesma construiu; cada ponto de composição é um membro, incluindo cada aplicação que carrega o módulo. Duas saídas resolvem: uma prova em cada lugar, ou uma composição compartilhada pelos dois caminhos.

## Checks executados

Use os comandos pertinentes da mudança e do repositório. Reaproveite resultados válidos para o mesmo conteúdo. Quando executar testes, registre comando, exit code e contagens disponíveis de aprovados, falhos e ignorados. Testes ignorados não são evidência; zero testes não comprova comportamento, embora uma alteração documental possa dispensar testes de runtime.

A evidência de um requisito nomeia o teste que o decide. Confirme que cada teste nomeado aparece na saída como tendo executado: um filtro que não casa nenhum teste termina com sucesso em vários runners, e o resultado é um requisito verde sem teste algum por trás. Agrupe as execuções por alvo em vez de invocar o runner uma vez por requisito; a garantia se mantém enquanto cada teste nomeado aparecer individualmente no resultado.

Execute as provas no estado atual do código. Um resultado verde obtido em um commit anterior não diz nada sobre o commit atual, e o relatório de quem implementou não substitui a execução.

Uma limitação de ambiente não é sucesso nem prova de defeito no produto; descreva o check pendente e seu impacto. Corrija falhas introduzidas pela mudança e repita os checks atingidos.

## Falha preexistente

Para confirmar que uma falha já existia, compare com evidência equivalente da base ou execute o mesmo check na base, numa worktree temporária que não toca o checkout do usuário:

1. `git worktree add <dir> <base>`, com `<dir>` inexistente e fora da árvore do repositório.
2. Execute o check dentro de `<dir>`.
3. Remova com `git worktree remove --force <dir>`. O `--force` descarta os artefatos de build que o passo 2 deixou; o diretório só contém o que os passos 1 e 2 criaram.

Sem essa confirmação, reporte a origem da falha como incerta; ela continua impedindo declarar a mudança verificada. Se só a remoção da worktree falhar, o resultado na base continua valendo; informe o diretório que ficou.

## Injeção de falha

Uma suíte verde prova que os testes executam, não que eles detectariam uma regressão. Injetar falha é o que produz essa informação, e não depende de ferramenta: inverta uma condição, troque um valor ou um status retornado, desloque um limite, remova um efeito exigido, e confirme que a prova mais estreita daquele requisito falha. Injete conforme o risco do que a mudança sustenta, o pedido e a regra do projeto, e declare no relatório se houve injeção e, quando não houve, por quê — sem essa linha, uma verificação que decidiu não injetar se lê igual a uma que esqueceu.

Aplique a mutação numa worktree temporária sobre `HEAD`, com o mesmo procedimento da confirmação de falha preexistente, e registre antes `git status --porcelain` da árvore real, para conferir ao remover a worktree que ela continua igual. Não use `git stash` para isolar a mutação: o stash guarda o estado anterior à alteração, então desempilhar não desfaz a falha injetada, e numa árvore limpa ele não cria entrada nenhuma.

Escolha uma falha por superfície de asserção distinta, não por linha arriscada; mutações que as mesmas provas matam repetem o mesmo experimento. Pare quando cada prova que sustenta um requisito tiver falhado uma vez. Onde a stack tiver ferramenta de mutação disponível ou autorizada, use-a — ela obtém muitos mutantes de uma execução — e registre comando e escopo.

Um mutante sobrevivente é achado, não nota de rodapé: a asserção passaria sob uma implementação errada. Analise antes de concluir, porque a sobrevivência também pode indicar equivalência de comportamento.

## Conformidade com o design

Confira responsabilidades, contratos, dependências, fronteiras, eventos, persistência e mitigação dos riscos descritos. Arquivos adicionais necessários à integração precisam de justificativa registrada. Mudanças que alterem comportamento voltam à fonte do contrato; não sobrevivem apenas como observação de revisão.

Revise se o diff contém trabalho fora do pedido, abstrações sem necessidade, opções sem consumidor ou mudanças adjacentes indevidas. Uma abstração usada uma vez pode ter motivo concreto; avalie-o, sem proibição baseada apenas em contagem.

## Correções

Em implementação autorizada, corrija as lacunas executáveis e repita a verificação pertinente. Registre tarefas de correção quando a decomposição ajudar. Em pedido apenas de revisão, entregue os achados sem iniciar implementação. Se as mesmas lacunas persistirem depois de uma rodada de correção, leve o diagnóstico ao usuário em vez de repetir o ciclo.

## Entrega

Comece pelo resultado e pela cobertura conhecida. Apresente checks executados, ressalvas do design, lacunas ordenadas pelo impacto e a ação necessária para resolvê-las. Distinga observação, hipótese e verificação não executada. Não transforme inspeção estática em prova de runtime nem uma nota de confiança em aprovação do produto.
