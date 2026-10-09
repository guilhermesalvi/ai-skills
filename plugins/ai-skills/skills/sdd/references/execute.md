# Execução

Implemente o escopo pedido e verifique o contrato. Conclua quando cada check do escopo tiver prova executada e verde; informe checks pendentes e seu impacto quando uma restrição impedir a conclusão.

## Antes de alterar

- Confira `git status`, o plano, a spec atual e as regras dos diretórios atingidos.
- Preserve o trabalho alheio.
- Sem spec para o comportamento alterado, leia [especificação](specify.md) e registre o contrato antes de planejar.
- Para criar ou ajustar o plano, leia [plano](plan.md). Sem plano da mudança, escreva-o antes de implementar.
- Sem uma branch própria para a mudança, registre em Context do plano a base de comparação, a saída de `git rev-parse HEAD`, antes de implementar.
- Leia [preparação](prepare.md) e resolva o que faltar para a parte que será implementada. Reutilize as decisões, dependências e fontes já confirmadas nos artefatos.

Use como base de comparação o commit contra o qual o diff será medido: o `HEAD` registrado antes da mudança ou, para uma branch própria, `git merge-base HEAD <branch principal>`.

## Implementar

- Use as dependências de Execution, quando presente, para escolher o próximo item pronto. Sem essa seção, derive a ordem das dependências reais e das convenções do repositório.
- Avance em fatias que possam se integrar e tenham seus próprios checks.

Em cada fatia, nesta ordem:

1. **Prepare as provas a partir dos checks e da spec.** Use testes existentes quando cobrirem o contrato; escreva os que faltarem. Consulte o código para integrar a prova, mas derive os resultados esperados do contrato.
2. **Implemente a menor solução** que satisfaça o contrato e as regras locais.
3. **Execute as provas**, inspecione o resultado e corrija as falhas introduzidas. Uma falha repetida sem evidência nova exige diagnóstico ou a explicitação do bloqueio, não tentativas idênticas.
4. **Marque o check** só depois de ver a prova passar sobre o conteúdo atual. Prova não executada deixa o check pendente.

Depois de integrar uma fatia, execute também os checks anteriores que a mudança possa ter afetado. Ao concluir, execute a [verificação](verify.md) sobre o escopo completo; provas isoladas dos itens não substituem a prova do comportamento de início ao fim.

## Limites

- Num pedido restrito a parte do plano, não amplie o escopo para pré-requisitos não autorizados: informe o impedimento e avance no que for independente.
- Não enfraqueça uma asserção nem apague ou pule um teste para a suíte passar.
- Um check que se revela errado volta à spec ou ao plano com o motivo.
- Valide a existência e a procedência de um pacote antes de adicioná-lo, e respeite as permissões de instalação e de acesso externo.
- Segredos e dados de produção não entram em respostas, exemplos, commits ou logs de teste.

## Desvios e restrições

- Uma restrição descoberta pode exigir corrigir a spec ou o plano. Registre o efeito material e continue o escopo autorizado.
- Reavalie apenas os itens, dependências e checks afetados pela descoberta, conforme [preparação](prepare.md#ajustar-com-novas-evidências).
- Atualize a spec ou o plano quando a decisão mudar, antes de implementar o comportamento ou a solução correspondente. Quando houver commit autorizado, agrupe o artefato com a mudança que ele descreve.
- Uma decisão irreversível descoberta na implementação entra em Technical Decisions do plano antes do código que a fecha, no formato do [plano](plan.md).

## Retomar uma mudança

- Reconstrua o estado pelo plano, pelos requisitos, pelas evidências e pelo diff já entregue, não por um resumo narrativo.
- Confira a prontidão do próximo trabalho e as dependências de Execution, quando presente. Complete o contexto ausente nas fontes antes de usar uma interface ou decisão inferida.
- Use o diff como evidência do que foi implementado. Quando ele divergir da spec ou do plano, confronte a divergência com o pedido: corrija o código que viola o contrato ou registre uma decisão autorizada que ainda não chegou ao documento.
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
