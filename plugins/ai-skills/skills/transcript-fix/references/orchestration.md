# Orquestração

## Papéis e capacidade

| Papel | Responsabilidade |
|---|---|
| Coordenador | Escopo, plano, conciliação do glossário, revisão do piloto, escalonamento e aceitação final |
| Executor | Extração de candidatos ou correção fiel de um trecho, sob contrato fixo |
| Executor de escalonamento | Reparar a tarefa em que o executor falhou, sem refazer trechos aprovados |

Escolha dinamicamente os modelos e parâmetros conforme a interface de colaboração disponível na sessão. O coordenador planeja e revisa; escolha o modelo executor mais leve disponível e faça-o passar pelo piloto antes de distribuí-lo ao restante. Se uma falha específica persistir, escale somente essa tarefa para uma capacidade mais forte ou faça-a você mesmo; um modelo ou esforço diferente exige novo piloto antes de distribuir novas tarefas. Respeite a preferência explícita do usuário. Não fixe IDs, aliases ou classificações de modelo nesta skill, nem presuma que todas as versões do Claude Code oferecem a mesma API. Não troque o modelo da sessão nem alegue um model switch que não ocorreu. Executores não lançam outros subagentes, ainda que a plataforma permita: toda distribuição parte do coordenador. Sem informação de preço, não alegue economia medida.

Quando a ferramenta disponível for `Agent` e expuser estes parâmetros, uma chamada independente pode usar:

```json
{
  "description": "corrigir trecho 03",
  "prompt": "<prompt autocontido com etapa, caminhos absolutos, contrato e saída>",
  "subagent_type": "<tipo com leitura e escrita de arquivos>",
  "model": "<modelo aceito pela interface>"
}
```

Escolha um `subagent_type` que comece com contexto próprio: um fork herda a conversa inteira e desfaz o isolamento que este fluxo exige. Os nomes e parâmetros aceitos vêm da interface efetivamente disponível; não trate este exemplo como contrato universal, não finja isolamento e não invente uma troca de modelo. Se não houver delegação disponível, aplique a seção [Sem subagentes](#sem-subagentes).

## Plano da execução

Antes de distribuir, grave `work/<run>/plan.json` com fonte e manifesto; palestrante e domínio quando conhecidos; os IDs efetivos de modelo e níveis de esforço de cada papel, conforme retornados ou aceitos pela interface, e a justificativa; cópias do glossário e recibo de consolidação; ID do piloto; e, por trecho, entradas, saídas, exceções contextuais, estado e tentativas. O plano registra a execução, não é configuração reutilizável. Ao retomar, valide os arquivos antes de confiar no estado registrado. Para recuperar uma consolidação interrompida, a referência é o recibo gravado antes da troca atômica do glossário, não o estado do plano.

## Contrato de cada tarefa

O prompt de cada executor é sempre autocontido e traz:

- a etapa e o ID do trecho, com caminhos absolutos de entrada e as saídas exclusivas;
- o prompt de `references/` preenchido, com metadados da fonte e o caminho do glossário imutável;
- o formato da saída e os critérios de aceitação;
- os limites: contexto só para leitura, sem editar fonte, glossário, plano ou outros trechos;
- o retorno esperado: resumo curto do resultado ou bloqueio específico.

Não copie esta conversa para o prompt. Quando a interface suportar isolamento de contexto, habilite-o; quando não suportar, limite explicitamente o executor aos arquivos e instruções do contrato. Crie as pastas de saída antes de distribuir. Lance tarefas independentes em paralelo somente dentro da capacidade disponível e acompanhe cada ID retornado. Aguarde a conclusão e confirme o término ou interrompa a tarefa anterior antes de reatribuir sua saída; nunca deixe duas tentativas escreverem no mesmo caminho.

## Piloto, aceitação e novas tentativas

Comece cada etapa por um trecho difícil e representativo. No piloto de extração, confira formato, graus de evidência e uma amostra curta da fonte. Depois de conciliar o glossário, faça o piloto de correção no mesmo trecho e exija sequência de horários preservada, nenhuma omissão ou invenção, incertezas marcadas corretamente e registro de alterações válido. Aprovar a extração não aprova a correção. Distribua o restante só depois do piloto aceito, com o mesmo modelo e nível de esforço aprovados no piloto, plano e glossário. Se qualquer um deles mudar, faça e aceite um novo piloto antes de distribuir.

Depois de cada etapa, confira todos os trechos do manifesto e espere todas as saídas antes de consolidar o glossário ou reunir o texto. Executor que não gravou a saída não concluiu a tarefa, mesmo que tenha respondido.

Dê ao executor que falhou uma nova tentativa com os achados exatos da validação. Se falhar de novo, escale só aquela tarefa para uma capacidade mais forte ou faça-a você mesmo. Se o mesmo bloqueio persistir, relate o trecho e preserve o restante, sem enfraquecer a fidelidade. Trechos menores exigem novo manifesto numa nova pasta `work/<run>`, para não misturar saídas.

Revise a fidelidade dos trechos sinalizados e de uma pequena amostra dos aprovados; amplie a revisão só quando as falhas indicarem um problema mais amplo. Os relatórios provam integridade estrutural; terminologia e sentido são responsabilidade do coordenador.

## Sem subagentes

Aplique os mesmos prompts você mesmo, um trecho por vez, com os mesmos contratos de arquivos, glossário imutável por etapa e validação final. Não alegue contexto novo, isolamento ou troca de modelo que não aconteceram. Preserve as saídas exclusivas, o piloto por etapa, os relatórios e os invariantes do glossário.
