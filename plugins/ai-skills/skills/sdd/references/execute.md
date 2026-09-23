# Execução

Implemente o escopo pedido até sua verificação. Cada unidade combina código, integração e evidência do comportamento exigido.

## Antes de alterar

Confira `git status`, o plano, a spec atual e as regras dos diretórios atingidos. Preserve o trabalho alheio.

Sem uma branch própria para a mudança, registre a base de comparação antes da primeira alteração, no `tasks.md` ou no plano: a saída de `git rev-parse HEAD`. A verificação usa essa base para isolar o diff da mudança.

Sem `tasks.md`, comece com um plano curto na resposta, com requisitos, estrutura, passos e verificação, e siga para a implementação. Uma nova decisão de produto continua exigindo resposta antes da parte dependente.

## Implementar uma unidade

1. **Escolha a tarefa.** Use a próxima disponível conforme as dependências, ou a que foi explicitamente pedida. Num pedido restrito a uma tarefa, não amplie o escopo para pré-requisitos não autorizados: informe o impedimento e avance no que for independente.
2. **Explique o caminho.** Diga quais são os arquivos principais, a abordagem e a verificação. Se descobrir um arquivo de registro, configuração ou integração indispensável, inclua-o no escopo da tarefa e atualize o plano com o motivo.
3. **Prepare os casos de teste.** Cada comportamento exigido tem uma asserção sobre o resultado que a spec define.
4. **Implemente a menor solução** que satisfaça o contrato e as regras locais. Não acrescente flexibilidade sem consumidor nem refatore áreas adjacentes sem necessidade.
5. **Execute os checks apropriados**, inspecione o resultado e corrija as falhas introduzidas. Uma falha repetida sem evidência nova exige diagnóstico ou a explicitação do bloqueio, não tentativas idênticas indefinidas.
6. **Confira os critérios de conclusão e o diff** contra a versão atual dos artefatos e do código. Associe cada resultado esperado à evidência executada. Marque uma tarefa como concluída apenas se seus critérios estiverem satisfeitos: teste não executado permanece pendente.

Ao concluir as unidades, execute a [verificação](verify.md).

## Desvios e restrições

Uma restrição descoberta pode exigir corrigir spec, design ou tarefas. Registre o efeito material e continue o escopo autorizado. Se a mudança implicar novo comportamento de produto, obtenha a decisão correspondente e mantenha o restante em andamento.

Uma divergência estrutural justificada pode ficar em Deviations ou na descrição da tarefa.

Valide a existência e a procedência de um pacote antes de adicioná-lo, e respeite as permissões de instalação e de acesso externo. Segredos e dados de produção não entram em respostas, exemplos, commits ou logs de teste.

## Retomar uma mudança

Leia o plano, os requisitos, as evidências e o estado atual. Checkboxes indicam o que foi registrado, mas não provam que mudanças posteriores continuam válidas. Reutilize a evidência para o mesmo conteúdo e repita apenas os checks afetados por diferenças relevantes.

Sem plano disponível, reconstrua o próximo passo com o que for comprovável. Não invente decisões, hashes ou testes já executados.

Resuma resultado, evidência e pendências reais. Um pedido de continuação mantém o objetivo e a autorização anteriores, salvo mudança explícita do usuário.
