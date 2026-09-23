# Fluxo e limites

## Dimensionar os artefatos

Defina o comportamento antes de implementá-lo. Reutilize uma spec existente ou registre o contrato necessário para a mudança; não crie arquivos vazios.

Sem convenção do repositório, use este layout, com slugs em inglês e em kebab-case:

```text
docs/specs/<context>/<capability>/
  spec.md              spec viva da capability, editada no lugar
  NNNN-<change>/       só quando a mudança tem design ou tarefas
    design.md
    tasks.md
docs/adr/NNNN-<decision>.md
```

`NNNN` é o próximo número livre na pasta. Se branches paralelos usarem o mesmo número, renumere o item que entrar depois e atualize quem o cita. Preserve outra organização já estabelecida no repositório. Planos técnicos duráveis ficam com os artefatos da mudança, não numa pasta de planos independente.

A quantidade de arquivos ou de exemplos encontrados não decide sozinha o tamanho do processo. Se o trabalho revelar depois a necessidade de um desses artefatos, produza-o e ajuste os dependentes.

## Escopo e autorização

O pedido define as etapas autorizadas:

- **Pedido de spec, design ou tarefas.** Termina no artefato.
- **Pedido de implementação.** Autoriza a spec que faltar, o planejamento necessário, a execução, a verificação e as correções dentro do escopo, sem aprovações intermediárias.

Artefatos ainda sem commit valem como entrada; registre qual versão a implementação usou. Commit e push seguem a autorização do usuário e não liberam etapas.

Decida por conta própria as escolhas técnicas reversíveis dentro do escopo. Pergunte quando faltar uma decisão indispensável de produto ou uma informação que o contexto não resolve, e continue o trabalho independente enquanto espera.

Corrija o que a sua mudança quebrar e os problemas preexistentes do trecho alterado que tenham o mesmo motivo da mudança. Os demais entram como sugestão no fim, sem alteração. Não acrescente complexidade sem necessidade concreta.

## Precedência

O pedido da sessão prevalece sobre as convenções do repositório, e ambos prevalecem sobre os defaults desta skill. Convenção é a regra escrita no `CLAUDE.md` ou em outra instrução do repositório; um padrão apenas observado em arquivos existentes não obriga, mas preserve-o ao editá-los.

Se uma regra local parecer impedir o trabalho, informe o arquivo, a regra e a ação afetada.

## Fatos, hipóteses e correções

Marque o que ainda não é fato:

- `[ASSUMPTION]` para inferência, com origem, escolha provisória e consequência.
- `[GAP]` para informação ou decisão ausente.

Um fato deve apontar para evidência no pedido, no PRD, no código ou na documentação. Verifique informações técnicas atuais nas fontes oficiais quando necessário; não invente APIs, ferramentas ou comportamento.

Corrija a inconsistência na origem dela: regra de negócio no PRD, comportamento técnico na spec, decisão estrutural no design. Depois atualize os consumidores afetados. Uma mudança de comportamento encontrada na verificação segue o mesmo caminho; ela não sobrevive apenas como observação de revisão.

Não altere o contrato para fazer um teste passar, nem refaça todo o fluxo por causa de um defeito local.

## Revisar um artefato

Revise spec, design, tarefas ou ADR contra a referência da etapa, com profundidade proporcional à mudança, e confira também:

- Caminhos, links e IDs resolvem para as fontes corretas; a numeração não colide e IDs retirados não voltam.
- Idioma, rótulos e formato existentes foram preservados, e cada seção tem conteúdo útil.
- Nenhum placeholder finge que uma decisão foi tomada, e nenhum exemplo aparece como evidência executada.
- Diagramas têm estrutura coerente, e o relatório diferencia inspeção textual de renderização.

## Idioma

A prosa segue o idioma fixado pelo pedido ou pela convenção do repositório; sem essa definição, o do PRD ou do material de origem.

Títulos de seção, campos de tarefa, tags e rótulos de linha mantêm a forma em inglês documentada nas referências. Nomes de APIs, tipos, paths e identificadores não se traduzem.
