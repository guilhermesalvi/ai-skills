# Verificação

Confronte a implementação com a spec e o plano atuais. Informe quais requisitos têm evidência, quais estão sem cobertura e quais ainda não definem um resultado preciso.

- O relatório normalmente vai na resposta.
- Salve um artefato quando o pedido ou a necessidade de rastreabilidade justificar.

Conteúdo: Base e leitura crítica · Revisor separado · Conformidade com a spec · Cobertura dos conjuntos · Checks executados · Falha preexistente · Conformidade com o plano · Correções · Injeção de falha · Relatório

## Base e leitura crítica

- Compare contra a base da mudança, incluindo os arquivos novos autorizados.
- A base é a registrada em Context do plano antes da primeira alteração ou, com branch própria, `git merge-base HEAD <branch principal>`.
- O último commit da spec não serve de base, porque uma spec viva acumula mudanças diferentes.
- Se não for possível recuperar a base, declare que a ausência de regressão não está demonstrada e verifique o estado atual sem inventar uma origem.
- Preserve as alterações alheias: a revisão não exige `add`, `stash`, restauração nem troca de checkout.
- Leia os requisitos e os testes antes de consultar a conclusão de quem implementou, para reduzir a confirmação automática da própria solução.

## Revisor separado

- Numa mudança não trivial, verifique em contexto separado de quem implementou sempre que houver subagente disponível, porque o autor tende a reaplicar o raciocínio que produziu a falha.
- Passe ao subagente os caminhos da spec e do plano, a base, os comandos de verificação e todos os requisitos de Requirements in Scope, não só a última fatia implementada.
- Com subagente, a entrega espera o resultado dele: sem esse resultado, a mudança não está verificada.
- Sem subagente, verifique mesmo assim e declare no relatório que autor e revisor são o mesmo.

## Conformidade com a spec

| Requisito | Resultado esperado | Evidência | Situação |
| --- | --- | --- | --- |
| ID em escopo | Estado, valor, erro ou evento definido | `arquivo:linha`, asserção e resultado do check | Coberto, sem cobertura ou requisito impreciso |

- A asserção precisa observar o resultado exigido. A existência de um teste qualquer não basta.
- Antes de declarar ausência, procure o ID e os identificadores de estado, erro ou evento nos testes pertinentes.
- Cite `arquivo:linha` e a expressão da asserção que decide o requisito.
- Se o valor esperado não for legível na asserção, porque vem de uma fixture montada em outro arquivo, registre isso como achado sobre o teste.
- Um teste prova a camada em que asserta, não as que atravessa. Um requisito que cita status HTTP, rota ou formato de resposta e só tem evidência abaixo dessa fronteira tem evidência no nível errado: divida o requisito ou acrescente a evidência no nível exigido.
- Um requisito sem evidência fica sem cobertura. Um requisito sem resultado definido volta à spec.
- Para um comportamento retirado, confira a remoção do caminho de código e o ajuste correspondente dos testes.
- Reorganizar testes pode mudar sua contagem sem reduzir a cobertura: investigue o motivo em vez de tratar toda redução como regressão automática.

## Cobertura dos conjuntos

- Um requisito sobre um conjunto só está coberto quando cada membro tem evidência. Uma prova que percorre o conjunto inteiro vale pela linha.
- Dê uma linha a cada conjunto que a mudança precisa cobrir, com o tamanho, e escreva cada membro ao lado da evidência que o observa.

| Conjunto e tamanho | Membro e evidência | Sem evidência |
| --- | --- | --- |
| Status do provedor (9) | EXM-04, prova por tabela sobre os 9 | `-` |
| Tipos de evento recebidos (4) | `paused` EXM-05 · `updated` EXM-06 · `deleted` EXM-07 · `trial_end` EXM-08 | `-` |

- Parta dos conjuntos, não dos testes escritos: resumir os testes não encontra membro sem teste.
- Tire os membros de quem tem autoridade sobre o conjunto, como o provedor, o framework, o plano ou o contrato, e não da implementação, que sempre se declara completa.
- Os pontos de composição da aplicação também formam um conjunto: cada aplicação que monta o módulo precisa de prova própria ou de uma composição compartilhada com a suíte.

## Checks executados

- Use os comandos pertinentes da mudança e do repositório.
- Reaproveite resultados válidos só para o mesmo conteúdo. O relatório de quem implementou não substitui a execução.
- Confirme na saída que cada teste citado como evidência executou: em vários runners, um filtro que não casa nenhum teste termina com sucesso.
- Agrupe as execuções por alvo em vez de invocar o runner uma vez por requisito.
- Registre comando, exit code e as contagens disponíveis de aprovados, falhos e ignorados.
- Testes ignorados não são evidência, e zero testes não comprova comportamento. Uma alteração documental pode dispensar testes de runtime.
- Uma limitação de ambiente não é sucesso nem prova de defeito no produto: descreva o check pendente e seu impacto.
- Corrija as falhas introduzidas pela mudança e repita os checks atingidos.

## Falha preexistente

Para confirmar que uma falha já existia, compare com evidência equivalente da base ou execute o mesmo check na base, numa worktree temporária que não toca o checkout do usuário:

1. `git worktree add <dir> <base>`, com `<dir>` inexistente e fora da árvore do repositório.
2. Execute o check dentro de `<dir>`.
3. Remova com `git worktree remove --force <dir>`. O `--force` descarta os artefatos de build que o passo 2 deixou; o diretório só contém o que os passos 1 e 2 criaram.

- Sem essa confirmação, reporte a origem da falha como incerta. Ela continua impedindo declarar a mudança verificada.
- Se apenas a remoção da worktree falhar, o resultado na base continua valendo. Informe o diretório que ficou.

## Conformidade com o plano

- Confira as decisões técnicas, responsabilidades, contratos, dependências, fronteiras, eventos, persistência e mitigação dos riscos descritos.
- Arquivos adicionais necessários à integração precisam de justificativa registrada.
- Revise se o diff contém trabalho fora do pedido, abstrações sem necessidade, opções sem consumidor ou mudanças adjacentes indevidas.
- Uma abstração usada uma vez pode ter motivo concreto: avalie-o, em vez de proibi-la pela contagem de usos.

## Correções

- Em implementação autorizada, corrija os achados executáveis e repita a verificação pertinente.
- Um requisito que ficou sem cobertura e foi corrigido ganha no plano o check que o prova.
- Em pedido apenas de revisão, entregue os achados sem iniciar implementação.
- Se os mesmos achados persistirem depois de uma rodada de correção, leve o diagnóstico ao usuário em vez de repetir o ciclo.

## Injeção de falha

Uma suíte verde prova que os testes executam, não que detectariam uma regressão.

- Numa mudança não trivial, injete falhas nas provas dos requisitos cujo erro custaria dinheiro, dado, conformidade ou um contrato publicado, e sempre que o pedido ou a regra do projeto pedir.
- Injete uma falha por superfície de asserção, como inverter uma condição, trocar um valor retornado, deslocar um limite ou remover um efeito exigido, e confirme que a prova mais estreita daquele requisito falha.
- Pare quando cada prova escolhida tiver falhado uma vez.
- Com ferramenta de mutação disponível ou autorizada, use-a e registre comando e escopo.
- Injete a falha numa worktree temporária sobre `HEAD`, com o procedimento de Falha preexistente. Se a mudança ainda não tiver commit, copie para a worktree os arquivos alterados e novos dela antes de injetar.
- Confira que o `git status --porcelain` da árvore real continua igual ao de antes.
- Não use `git stash` para isolar a falha: desempilhar não a desfaz, e numa árvore limpa o stash nem cria entrada.
- Um mutante sobrevivente é achado: a asserção passaria sob uma implementação errada, salvo se a análise mostrar equivalência de comportamento.
- Numa mudança não trivial, o relatório diz se houve injeção e, se não houve, por quê.

## Relatório

- Comece pelo resultado e pela cobertura conhecida.
- Apresente os checks executados, as ressalvas do plano, os achados ordenados pelo impacto e a ação necessária para resolvê-los.
- Distinga observação, hipótese e verificação não executada.
- Não transforme inspeção estática em prova de runtime, nem uma nota de confiança em aprovação do produto.
