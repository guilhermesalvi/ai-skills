# Fluxo e limites

## Dimensionar os artefatos

Defina o comportamento antes de implementá-lo. Reutilize uma spec existente ou registre o contrato necessário para a mudança; não crie arquivos vazios.

Sem convenção do repositório, use este layout, com slugs em inglês e kebab-case:

```text
docs/specs/<context>/<capability>/
  spec.md              spec viva da capability, editada no lugar
  NNNN-<change>/       só quando a mudança tem design ou tarefas
    design.md
    tasks.md
docs/adr/NNNN-<decision>.md
```

`NNNN` é o próximo número livre na pasta. Se branches paralelos usarem o mesmo número, renumere o item que entrar depois e atualize quem o cita. Preserve outra organização já estabelecida no repositório. Planos técnicos duráveis ficam com os artefatos da mudança, não numa pasta de planos independente.

Use design quando houver decisão relevante de arquitetura, contrato público, persistência, integração ou migração, ou risco que exija comparar soluções. Use tarefas quando a decomposição e as dependências precisarem de registro durável. Uma mudança pequena pode usar um plano curto na conversa. A quantidade de arquivos ou de exemplos encontrados não decide sozinha o tamanho do processo. Se o trabalho revelar depois a necessidade de um desses artefatos, produza-o e ajuste os dependentes.

| Etapa | Contexto necessário |
| --- | --- |
| Especificar | PRD, pedido com comportamento identificável ou código a documentar |
| Projetar | Contrato da spec, restrições pertinentes e código atingido |
| Decompor | Spec e design, quando necessário |
| Executar | Requisitos e plano com resultado e verificação definidos |
| Verificar | Escopo da mudança, artefatos atuais e evidências disponíveis |
| ADR | Decisão que estabelece regra ou restrição além da capability |

## Escopo e autorização

O pedido define as etapas autorizadas. Um pedido de spec, design ou tarefas termina no artefato. Um pedido de implementação autoriza a spec que faltar, o planejamento necessário, a execução, a verificação e as correções dentro do escopo, sem aprovações intermediárias. Artefatos ainda sem commit valem como entrada; registre qual versão a implementação usou. Commit e push seguem a autorização do usuário e não liberam etapas.

Decida escolhas técnicas reversíveis dentro do escopo. Pergunte quando faltar uma decisão indispensável de produto ou informação que o contexto não resolve, e continue o trabalho independente. Corrija o que a sua mudança quebrar e os problemas preexistentes do trecho alterado que tenham o mesmo motivo da mudança; os demais entram como sugestão no fim, sem alteração. Não acrescente complexidade sem necessidade concreta.

O pedido da sessão prevalece sobre as convenções do repositório, e ambos prevalecem sobre os defaults desta skill. Convenção é a regra escrita no `CLAUDE.md` ou em outra instrução do repositório; um padrão apenas observado em arquivos existentes não obriga, mas é preservado ao editá-los. Se uma regra local parecer impedir o trabalho, informe o arquivo, a regra e a ação afetada.

## Fatos, hipóteses e correções

Use `[ASSUMPTION]` para inferência com origem, escolha provisória e consequência; use `[GAP]` para informação ou decisão ausente. Marque quem decidiu no campo `Confirmed?`: `y` quando o usuário respondeu, inclusive ao delegar a escolha, e `n` para o default que ninguém viu. Sem essa marca, um default silencioso fica indistinguível de uma decisão tomada. Um fato deve apontar para evidência no pedido, PRD, código ou documentação. Verifique informações técnicas atuais nas fontes oficiais quando necessário; não invente APIs, ferramentas ou comportamento.

Corrija a origem de uma inconsistência: regra de negócio no PRD, comportamento técnico na spec, decisão estrutural no design. Atualize os consumidores afetados. Não altere o contrato para fazer um teste passar nem refaça todo o fluxo por causa de um defeito local.

## Idioma

A prosa segue o idioma fixado pelo pedido ou pela convenção do repositório; sem essa definição, o do PRD ou do material de origem. Títulos de seção, campos de tarefa, tags e rótulos de linha mantêm a forma em inglês documentada nas referências. Nomes de APIs, tipos, paths e identificadores não se traduzem.
