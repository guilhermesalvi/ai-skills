# Verificação

Confronte a implementação com a spec e o design atuais. Informe quais requisitos têm evidência, quais estão sem cobertura e quais ainda não definem um resultado preciso.

O relatório normalmente vai na resposta. Salve um artefato quando o pedido ou a necessidade de rastreabilidade justificar.

## Escopo e leitura crítica

Compare contra a base da mudança, incluindo os arquivos novos autorizados. A base é a que foi registrada antes da primeira alteração ou, com branch própria, `git merge-base HEAD <branch principal>`.

O último commit da spec não serve de base, porque uma spec viva acumula mudanças diferentes. Se não for possível recuperar a base, declare que a ausência de regressão não está demonstrada e verifique o estado atual sem inventar uma origem.

Preserve as alterações alheias: a revisão não exige `add`, `stash`, restauração nem troca de checkout.

Leia os requisitos e os testes antes de consultar a conclusão de quem implementou, para reduzir a confirmação automática da própria solução.

Uma revisão independente pode ajudar em mudanças extensas ou de risco alto: delegue a um subagente disponível, com os caminhos da spec, do design e do plano, a base e os comandos de verificação. A mera existência de capacidade de delegação não obriga seu uso. Declare o grau de independência quando ele for relevante à confiança no resultado.

## Conformidade com a spec

| Requisito | Resultado esperado | Evidência | Situação |
| --- | --- | --- | --- |
| ID em escopo | Estado, valor, erro ou evento definido | `arquivo:linha`, asserção e resultado do check | Coberto, lacuna de cobertura ou requisito impreciso |

A asserção precisa observar o resultado exigido; a existência de um teste qualquer não basta. Antes de declarar ausência, procure o ID e os identificadores de estado, erro ou evento nos testes pertinentes.

Um requisito sem evidência fica como lacuna de cobertura; um requisito sem resultado definido volta à spec.

Para um comportamento retirado, confira a remoção do caminho de código e o ajuste correspondente dos testes. Reorganizar testes pode mudar sua contagem sem reduzir a cobertura: investigue o motivo em vez de tratar toda redução como regressão automática.

## Checks executados

Use os comandos pertinentes da mudança e do repositório, e reaproveite resultados válidos para o mesmo conteúdo.

Quando executar testes, registre comando, exit code e as contagens disponíveis de aprovados, falhos e ignorados. Testes ignorados não são evidência, e zero testes não comprova comportamento, embora uma alteração documental possa dispensar testes de runtime.

Uma limitação de ambiente não é sucesso nem prova de defeito no produto: descreva o check pendente e seu impacto. Corrija as falhas introduzidas pela mudança e repita os checks atingidos.

## Falha preexistente

Para confirmar que uma falha já existia, compare com evidência equivalente da base ou execute o mesmo check na base, numa worktree temporária que não toca o checkout do usuário:

1. `git worktree add <dir> <base>`, com `<dir>` inexistente e fora da árvore do repositório.
2. Execute o check dentro de `<dir>`.
3. Remova com `git worktree remove --force <dir>`. O `--force` descarta os artefatos de build que o passo 2 deixou; o diretório só contém o que os passos 1 e 2 criaram.

Sem essa confirmação, reporte a origem da falha como incerta. Ela continua impedindo declarar a mudança verificada.

Se apenas a remoção da worktree falhar, o resultado na base continua valendo; informe o diretório que ficou.

## Conformidade com o design

Confira responsabilidades, contratos, dependências, fronteiras, eventos, persistência e mitigação dos riscos descritos. Arquivos adicionais necessários à integração precisam de justificativa registrada.

Revise se o diff contém trabalho fora do pedido, abstrações sem necessidade, opções sem consumidor ou mudanças adjacentes indevidas. Uma abstração usada uma vez pode ter motivo concreto: avalie-o, em vez de proibi-la com base apenas na contagem de usos.

## Correções

Em implementação autorizada, corrija as lacunas executáveis e repita a verificação pertinente. Registre tarefas de correção quando a decomposição ajudar. Em pedido apenas de revisão, entregue os achados sem iniciar implementação.

Se as mesmas lacunas persistirem depois de uma rodada de correção, leve o diagnóstico ao usuário em vez de repetir o ciclo.

## Mutation testing

Use mutation testing quando o usuário pedir, quando o projeto exigir ou quando o risco concreto justificar essa evidência e a ferramenta estiver disponível ou sua instalação autorizada. Registre comando e escopo.

Dinheiro, segurança ou concorrência pedem verificação adequada, mas não obrigam instalar uma ferramenta de mutação em toda mudança. Mutantes sobreviventes exigem análise, porque podem indicar lacuna de teste ou equivalência de comportamento.

## Entrega

Comece pelo resultado e pela cobertura conhecida. Apresente os checks executados, as ressalvas do design, as lacunas ordenadas pelo impacto e a ação necessária para resolvê-las.

Distinga observação, hipótese e verificação não executada. Não transforme inspeção estática em prova de runtime, nem uma nota de confiança em aprovação do produto.
