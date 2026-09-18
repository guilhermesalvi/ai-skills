# Execução

Implemente o escopo pedido até sua verificação. Cada unidade combina código, integração e evidência do comportamento exigido.

## Antes de alterar

Confira `git status`, o plano, a spec atual e as regras dos diretórios atingidos. Preserve o trabalho alheio.

Sem branch própria para a mudança, registre no `tasks.md` ou no plano, antes da primeira alteração, a base de comparação: a saída de `git rev-parse HEAD`. A verificação usa essa base para isolar o diff da mudança.

Sem `tasks.md`, comece com um plano curto na resposta, com requisitos, estrutura, passos e verificação, e siga para a implementação. Uma nova decisão de produto continua exigindo resposta antes da parte dependente.

## Implementar uma unidade

1. Escolha a próxima tarefa disponível conforme as dependências, ou a tarefa explicitamente pedida. Em um pedido restrito a uma tarefa, não amplie o escopo para pré-requisitos não autorizados; informe o impedimento e avance no que for independente.
2. Explique os arquivos principais, a abordagem e a verificação. Atualize o plano se descobrir um arquivo de integração indispensável, com o motivo.
3. Prepare os casos de teste da unidade. Cada comportamento exigido tem uma asserção sobre o resultado que a spec define.
4. Implemente a menor solução que satisfaça o contrato e as regras locais. Inclua registros, configuração e integração necessários; não acrescente flexibilidade sem consumidor nem refatore áreas adjacentes sem necessidade.
5. Execute os checks apropriados, inspecione o resultado e corrija falhas introduzidas. Uma falha repetida sem evidência nova exige diagnóstico ou explicitação do bloqueio, não tentativas idênticas indefinidas.
6. Confira os critérios de conclusão e o diff. Associe resultado esperado à evidência executada. Marque uma tarefa como concluída apenas se seus critérios estiverem satisfeitos; teste não executado permanece pendente.

## Desvios e restrições

Uma restrição descoberta pode exigir corrigir spec, design ou tarefas. Registre o efeito material e continue o escopo autorizado. Se a mudança implicar novo comportamento de produto, obtenha a decisão correspondente e mantenha o restante em andamento.

Corrija o artefato no commit que muda o comportamento descrito, não ao final. Um caminho, um componente ou um impacto descrito depois vira justificativa do que já foi feito, e um mapa que não corresponde ao código engana mais que a ausência dele. Uma decisão irreversível descoberta durante a implementação entra no design antes do código que a fecha, com a forma literal e a alternativa rejeitada: a alternativa só é conhecível enquanto a escolha ainda está aberta.

Uma divergência estrutural justificada pode ficar em Deviations ou na descrição da tarefa. Arquivos indispensáveis de registro ou configuração entram no escopo explicado da tarefa.

Valide a existência e a procedência de um pacote antes de adicioná-lo. Respeite as permissões de instalação e acesso externo. Segredos e dados de produção não entram em respostas, exemplos, commits ou logs de teste.

## Encerrar a implementação

Confronte a versão atual dos artefatos e do código; não teste uma versão antiga para contornar uma diferença. Execute a [verificação](verify.md) ao concluir as unidades.

## Retomar uma mudança

Leia o plano, requisitos, evidências e estado atual. Checkboxes indicam o que foi registrado, mas não provam que mudanças posteriores continuam válidas. Reutilize evidência para o mesmo conteúdo e repita apenas os checks afetados por diferenças relevantes.

Reconstrua o estado a partir dos artefatos e do diff do que já foi entregue, não de um resumo narrativo do trabalho. O diff carrega as escolhas reversíveis que nenhum documento registra — nomes, formato de erro, onde o helper ficou — e é justamente o que um resumo perde. Onde os dois discordarem, o diff decide e o registro desatualizado é corrigido.

Depois de uma compactação de contexto, releia os artefatos da mudança e o diff antes de continuar. Não dá para perceber o limite se aproximando, mas dá para perceber que a compactação ocorreu, e é esse o sinal disponível.

Sem plano disponível, reconstrua o próximo passo com o que for comprovável; não invente decisões, hashes ou testes já executados. Se a base do diff for desconhecida, informe a limitação da comparação e procure recuperá-la. Ainda é possível avaliar o comportamento atual; não declare demonstrada uma ausência de regressão sem base.

Resuma resultado, evidência e pendências reais. Um pedido de continuação mantém o objetivo e a autorização anteriores, salvo mudança explícita do usuário.

Quando outro executor ou outra sessão continuar o trabalho, registre no `tasks.md` ou no plano a fronteira alcançada, o que o usuário decidiu durante a implementação e o que foi tentado e descartado. Escrito apenas no pedido de continuação, esse contexto sobrevive a uma troca e desaparece na seguinte.
