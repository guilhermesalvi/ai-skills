# Fluxo e limites

## Dimensionar os artefatos

Defina o comportamento antes de implementá-lo. Reutilize uma spec existente ou registre o contrato necessário para a mudança; não crie arquivos vazios.

Sem convenção do repositório, use este layout, com slugs em inglês e em kebab-case; o slug da capability repete o do PRD dela, quando houver:

```text
docs/specs/<capability>/
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

Um fato deve apontar para evidência no pedido, no PRD, no código ou na documentação. Verifique informações técnicas atuais nas fontes oficiais quando necessário; não invente APIs, ferramentas ou comportamento.

O que ainda não é fato vai para a seção Premissas ou para a seção Lacunas do artefato onde a questão surge: a spec, para comportamento, e o design, para a solução.

Uma premissa é uma inferência ou uma escolha provisória que o trabalho usa. A entrada registra a origem, a escolha, a consequência se ela for falsa e o campo `Confirmada?`: `s` quando o usuário decidiu, inclusive ao delegar a escolha, e `n` para o default que ninguém viu. Sem esse campo, um default silencioso parece decisão tomada. O texto que depende da premissa a apresenta como hipótese, não como fato.

Uma lacuna é uma informação ou decisão ausente. A entrada registra o que falta, os requisitos bloqueados e quem decide. O corpo do artefato afirma só o que está decidido, e um requisito que depende inteiramente de uma lacuna só é escrito quando ela for resolvida.

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

Títulos de seção, campos de tarefa e rótulos acompanham o idioma da prosa, sem misturar idiomas no mesmo artefato; um artefato existente conserva o idioma dos seus títulos. Esta skill os nomeia em português; num artefato em inglês, use a coluna English da tabela abaixo.

Nomes de APIs, tipos, paths e identificadores não se traduzem, nem termos canônicos como EARS, NFR, trade-off e Gate.

| Artefato | Português | English |
| --- | --- | --- |
| Spec e design | Premissas, Lacunas, campo `Confirmada?` com `s` ou `n` | Assumptions, Gaps, field `Confirmed?` with `y` or `n` |
| Spec | Prefixo dos requisitos, PRD de origem, Contexto, Escopo / Fora do escopo, Requisitos, Decisões observáveis, Eventos de domínio, Glossário, Rastreabilidade, Divergências, `Retirados:` | Requirement Prefix, Source PRD, Context, Scope / Out of Scope, Requirements, Observable, Domain Events, Glossary, Traceability, Divergences, `Retired:` |
| Design | Contexto do design, Critérios de avaliação, Riscos e técnicas, Abordagens, Visão da arquitetura, Unidade de implantação, Componentes, Eventos de domínio, Modelo de dados, Tratamento de erros, Decisões técnicas, Arquivos a criar ou alterar | Design Context, Evaluation Criteria, Risks and Techniques, Approaches, Architecture Overview, Deployment Unit, Components, Domain Events, Data Model, Error Handling, Technical Decisions, Files to Create or Modify |
| Tarefas | Comandos de gate, Plano de execução, Tarefas, Rastreabilidade, Desvios, Tarefas de correção; campos O quê, Onde, Depende de (`nenhuma`), Requisitos, Interfaces, Pronto quando, Testes, Gate | Gate Commands, Execution Plan, Tasks, Traceability, Deviations, Correction Tasks; fields What, Where, Depends on (`none`), Requirement, Interfaces, Done when, Tests, Gate |
| ADR | `ADR NNNN: decisão`, Participantes, Contexto, Decisão, Alternativas consideradas, Consequências, Regras derivadas, `Substitui: NNNN`, `Substituído por: NNNN` | `ADR NNNN: decision`, Participants, Context, Decision, Alternatives considered, Consequences, Derived rules, `Supersedes: NNNN`, `Superseded by: NNNN` |
