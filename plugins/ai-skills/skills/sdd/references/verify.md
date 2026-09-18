# Verificação

Confronte a implementação com a spec e o design atuais. Informe quais requisitos têm evidência, quais estão sem cobertura e quais ainda não definem um resultado preciso. O relatório normalmente vai na resposta; salve um artefato quando o pedido ou a necessidade de rastreabilidade justificar.

## Escopo e leitura crítica

Compare contra a base da mudança, incluindo arquivos novos autorizados. Use a base registrada antes da primeira alteração ou, com branch própria, `git merge-base HEAD <branch principal>`. O último commit da spec não serve de base, porque uma spec viva acumula mudanças diferentes. Se não for possível recuperar a base, declare a limitação de regressão e verifique o estado atual sem inventar uma origem.

Preserve alterações alheias: a revisão não exige `add`, `stash`, restauração ou troca de checkout. Leia os requisitos e os testes antes de consultar a conclusão do implementador, para reduzir a confirmação automática da própria solução.

Uma revisão independente pode ajudar em mudanças extensas ou de risco alto: um subagente disponível, com os caminhos da spec, do design e do plano, a base e os comandos de verificação. A mera existência de capacidade de delegação não obriga seu uso. Declare o grau de independência quando ele for relevante à confiança no resultado.

## Conformidade com a spec

| Requisito | Resultado esperado | Evidência | Situação |
| --- | --- | --- | --- |
| ID em escopo | Estado, valor, erro ou evento definido | `arquivo:linha`, asserção e resultado do check | Coberto, lacuna de cobertura ou requisito impreciso |

A asserção precisa observar o resultado exigido; a existência de um teste qualquer não basta. Antes de declarar ausência, procure o ID e os identificadores de estado, erro ou evento nos testes pertinentes. Um requisito sem evidência fica como lacuna; um requisito sem resultado definido volta à spec.

Para um comportamento retirado, confira a remoção do caminho de código e o ajuste correspondente dos testes. Reorganizar testes pode mudar sua contagem sem reduzir a cobertura; investigue o motivo em vez de tratar toda redução como regressão automática.

## Checks executados

Use os comandos pertinentes da mudança e do repositório. Reaproveite resultados válidos para o mesmo conteúdo. Quando executar testes, registre comando, exit code e contagens disponíveis de aprovados, falhos e ignorados. Testes ignorados não são evidência; zero testes não comprova comportamento, embora uma alteração documental possa dispensar testes de runtime.

Uma limitação de ambiente não é sucesso nem prova de defeito no produto; descreva o check pendente e seu impacto. Corrija falhas introduzidas pela mudança e repita os checks atingidos.

## Falha preexistente

Para confirmar que uma falha já existia, compare com evidência equivalente da base ou execute o mesmo check na base, numa worktree temporária que não toca o checkout do usuário:

1. `git worktree add <dir> <base>`, com `<dir>` inexistente e fora da árvore do repositório.
2. Execute o check dentro de `<dir>`.
3. Remova com `git worktree remove --force <dir>`. O `--force` descarta os artefatos de build que o passo 2 deixou; o diretório só contém o que os passos 1 e 2 criaram.

Sem essa confirmação, reporte a origem da falha como incerta; ela continua impedindo declarar a mudança verificada. Se só a remoção da worktree falhar, o resultado na base continua valendo; informe o diretório que ficou.

## Conformidade com o design

Confira responsabilidades, contratos, dependências, fronteiras, eventos, persistência e mitigação dos riscos descritos. Arquivos adicionais necessários à integração precisam de justificativa registrada. Mudanças que alterem comportamento voltam à fonte do contrato; não sobrevivem apenas como observação de revisão.

Revise se o diff contém trabalho fora do pedido, abstrações sem necessidade, opções sem consumidor ou mudanças adjacentes indevidas. Uma abstração usada uma vez pode ter motivo concreto; avalie-o, sem proibição baseada apenas em contagem.

## Correções e mutação

Em implementação autorizada, corrija as lacunas executáveis e repita a verificação pertinente. Registre tarefas de correção quando a decomposição ajudar. Em pedido apenas de revisão, entregue os achados sem iniciar implementação. Se as mesmas lacunas persistirem depois de uma rodada de correção, leve o diagnóstico ao usuário em vez de repetir o ciclo.

Use mutation testing quando o usuário pedir, quando o projeto exigir ou quando o risco concreto justificar essa evidência e a ferramenta estiver disponível ou sua instalação autorizada. Registre comando e escopo. Dinheiro, segurança ou concorrência pedem verificação adequada, mas não obrigam instalar uma ferramenta de mutação em toda mudança. Mutantes sobreviventes exigem análise, pois podem indicar lacuna de teste ou equivalência de comportamento.

## Entrega

Comece pelo resultado e pela cobertura conhecida. Apresente checks executados, ressalvas do design, lacunas ordenadas pelo impacto e a ação necessária para resolvê-las. Distinga observação, hipótese e verificação não executada. Não transforme inspeção estática em prova de runtime nem uma nota de confiança em aprovação do produto.
