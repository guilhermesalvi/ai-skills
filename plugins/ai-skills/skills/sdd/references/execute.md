# Execução

Implemente o escopo pedido até sua verificação. O trabalho termina quando cada check do escopo tem a prova executada e verde, não quando o código compila.

## Antes de alterar

- Confira `git status`, o plano, a spec atual e as regras dos diretórios atingidos.
- Preserve o trabalho alheio.
- Sem plano da mudança, escreva-o antes da primeira alteração.
- Sem uma branch própria para a mudança, registre em Context do plano a base de comparação antes da primeira alteração: a saída de `git rev-parse HEAD`. A verificação usa essa base para isolar o diff da mudança.

## Implementar

- A ordem, os arquivos e a divisão em passos são decisão sua, guiada pelas dependências reais e pelas convenções do repositório.
- Avance em fatias coerentes, cada uma integrável e com seus checks.

Em cada fatia, nesta ordem:

1. **Escreva os testes a partir dos checks e da spec**, nunca lendo a implementação. Um teste derivado do código confirma o que ele faz, não o que o contrato exige.
2. **Implemente a menor solução** que satisfaça o contrato e as regras locais.
3. **Execute as provas**, inspecione o resultado e corrija as falhas introduzidas. Uma falha repetida sem evidência nova exige diagnóstico ou a explicitação do bloqueio, não tentativas idênticas.
4. **Marque o check** só depois de ver a prova passar sobre o conteúdo atual. Prova não executada deixa o check pendente.

Ao concluir, execute a [verificação](verify.md).

## Limites

- Num pedido restrito a parte do plano, não amplie o escopo para pré-requisitos não autorizados: informe o impedimento e avance no que for independente.
- Não enfraqueça uma asserção nem apague ou pule um teste para a suíte passar.
- Um check que se revela errado volta à spec ou ao plano com o motivo.
- Valide a existência e a procedência de um pacote antes de adicioná-lo, e respeite as permissões de instalação e de acesso externo.
- Segredos e dados de produção não entram em respostas, exemplos, commits ou logs de teste.

## Desvios e restrições

- Uma restrição descoberta pode exigir corrigir a spec ou o plano. Registre o efeito material e continue o escopo autorizado.
- Atualize a spec ou o plano no mesmo commit que muda o que eles descrevem, não ao final. Escrito depois, o registro vira justificativa do que já foi feito.
- Uma decisão irreversível descoberta na implementação entra em Technical Decisions do plano antes do código que a fecha, no formato do [plano](plan.md).

## Retomar uma mudança

- Reconstrua o estado pelo plano, pelos requisitos, pelas evidências e pelo diff já entregue, não por um resumo narrativo.
- Onde o diff e os documentos discordarem, o diff decide e o registro é corrigido, porque o diff carrega escolhas que nenhum documento registra.
- Checks marcados indicam o que foi registrado, mas não provam que mudanças posteriores continuam válidas. Reutilize a evidência para o mesmo conteúdo e repita apenas os checks afetados por diferenças relevantes.
- Depois de uma compactação de contexto, releia os artefatos da mudança e o diff antes de continuar.
- Sem plano disponível, reconstrua o próximo passo com o que for comprovável. Não invente decisões, hashes ou testes já executados.
- Um pedido de continuação mantém o objetivo e a autorização anteriores, salvo mudança explícita do usuário.
- Resuma resultado, evidência e pendências reais.

## Passar a mudança adiante

Quando outro executor ou outra sessão for continuar, registre em Progress do plano:

- a fronteira alcançada;
- as decisões do usuário durante a implementação;
- o que foi tentado e descartado, com o motivo.
