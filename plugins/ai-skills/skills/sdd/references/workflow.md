# Fluxo e limites

## Dimensionar os artefatos

Defina o comportamento antes de implementá-lo. Reutilize um PRD ou uma spec existente ou registre o contrato necessário para a mudança; não crie arquivos vazios.

Sem convenção do repositório, use este layout, com slugs em inglês e em kebab-case. A pasta de uma capability reúne o PRD, a spec e as mudanças dela:

```text
docs/specs/
  overview.md               visão geral de produto
  <capability>/
    prd.md                  PRD da capability, editado no lugar
    spec.md                 spec viva da capability, editada no lugar
    NNNN-<change>/          só quando a mudança tem design ou tarefas
      design.md
      tasks.md
docs/adr/NNNN-<decision>.md
```

O ADR fica fora das pastas de capability porque registra uma decisão que vale para outras capabilities.

`NNNN` tem quatro dígitos e é o número seguinte ao maior da pasta. Cada número pertence a um só item e não muda quando ele é revisado. Se branches paralelos chegarem ao mesmo número, mantenha o do item que já estava na branch de destino, dê ao outro o número seguinte ao maior da pasta e atualize quem o cita. Preserve outra organização já estabelecida no repositório. Planos técnicos duráveis ficam com os artefatos da mudança, não numa pasta de planos independente.

A quantidade de arquivos ou de exemplos encontrados não decide sozinha o tamanho do processo. Se o trabalho revelar depois a necessidade de um desses artefatos, produza-o e ajuste os dependentes.

## Documentos vivos

PRD e spec descrevem o contrato atual. Altere-os no próprio arquivo, sem cópia ou versão paralela: o diff registra a mudança, e o histórico do Git, a autoria e a evolução.

O andamento da implementação pertence às tarefas e à entrega; não o registre no PRD nem na spec. Ficam fora desses documentos, porque não descrevem o contrato:

- instruções dirigidas ao agente ou a quem edita o documento;
- histórico de revisões;
- campos de aprovação e status do documento, como rascunho, validado ou aprovado;
- resultado das verificações e da revisão, que a entrega informa na resposta;
- notas sobre a ferramenta que gerou ou editou o texto;
- exemplos que ilustram o método de escrita em vez do comportamento. Exemplos que especificam o comportamento, como tabelas de cálculo e casos de aceitação, continuam no documento.

## Escopo e autorização

O pedido define as etapas autorizadas:

- **Pedido de PRD, spec, design ou tarefas.** Termina no artefato.
- **Pedido de implementação.** Autoriza a spec que faltar, o planejamento necessário, a execução, a verificação e as correções dentro do escopo, sem aprovações intermediárias. Não autoriza criar um PRD nem mudar uma regra de negócio, porque essas decisões pertencem ao usuário.

Artefatos ainda sem commit valem como entrada; registre qual versão a implementação usou. Commit e push seguem a autorização do usuário e não liberam etapas.

Decida por conta própria as escolhas técnicas e editoriais reversíveis dentro do escopo. Pergunte quando faltar uma decisão indispensável de produto ou uma informação que o contexto não resolve, e continue o trabalho independente enquanto espera.

Corrija o que a sua mudança quebrar e os problemas preexistentes do trecho alterado que tenham o mesmo motivo da mudança. Os demais entram como sugestão no fim, sem alteração. Não acrescente complexidade sem necessidade concreta.

## Precedência

O pedido da sessão prevalece sobre as convenções do repositório, e ambos prevalecem sobre os defaults desta skill e do verificador. Convenção é a regra escrita no `CLAUDE.md` ou em outra instrução do repositório; um padrão apenas observado em arquivos existentes não obriga, mas preserve-o ao editá-los.

Se uma regra local parecer impedir o trabalho, informe o arquivo, a regra e a ação afetada.

## Fatos, premissas e lacunas

Um fato aponta para sua origem: decisão do usuário, regra formalizada, PRD, código, documentação, observação ou fonte pertinente. Verifique informações técnicas atuais nas fontes oficiais quando necessário; não invente APIs, ferramentas ou comportamento.

O que ainda não é fato vai para a seção Premissas ou para a seção Lacunas do artefato onde a questão surge: o PRD, para produto; a spec, para comportamento técnico; o design, para a solução.

Uma premissa é uma inferência ou uma escolha provisória que o trabalho usa. O texto que depende dela a apresenta como hipótese, não como fato, e a entrada registra a origem ou a evidência que a motivou e a consequência se ela for falsa. Na spec e no design, a entrada registra também a escolha e o campo `Confirmada?`: `s` quando o usuário decidiu, inclusive ao delegar a escolha, e `n` para o default que ninguém viu. Sem esse campo, um default silencioso parece decisão tomada. Os campos do PRD estão na seção Premissas e lacunas de [requisitos e seções](prd/writing.md).

Uma lacuna é uma informação ou decisão ausente. A entrada registra o que falta, os IDs afetados e quem decide. O corpo do artefato afirma só o que está decidido, e um requisito que depende inteiramente de uma lacuna só é escrito quando ela for resolvida. Não preencha uma lacuna com especulação: usuário, métrica, limite ou regra ausente continua lacuna, e inventar um valor só torna a frase aparentemente verificável.

Quando regras, fontes ou paráfrases se contradisserem, ou quando uma correção depender de decisão de negócio, registre a lacuna com os IDs afetados e conclua o restante. Não escolha uma das versões em silêncio.

Corrija a inconsistência na origem dela: regra de negócio no PRD, comportamento técnico na spec, decisão estrutural no design. Depois atualize os consumidores afetados. Uma mudança de comportamento encontrada na verificação segue o mesmo caminho; ela não sobrevive apenas como observação de revisão.

Não altere o contrato para fazer um teste passar, nem refaça todo o fluxo por causa de um defeito local.

## Revisar um artefato

Revise PRD, spec, design, tarefas ou ADR contra a referência da etapa, com profundidade proporcional à mudança, e confira também:

- Caminhos, links e IDs resolvem para as fontes corretas; a numeração não colide e IDs retirados não voltam.
- Idioma, rótulos e formato existentes foram preservados, e cada seção tem conteúdo útil.
- Nenhum placeholder finge que uma decisão foi tomada, e nenhum exemplo aparece como evidência executada.
- Diagramas têm estrutura coerente, e o relatório diferencia inspeção textual de renderização.

## Idioma

A prosa de um artefato novo segue o idioma fixado pelo pedido ou pela convenção do repositório. Sem essa definição, use o do PRD ou do material de origem e, sem material, o idioma em que o pedido foi escrito.

Títulos de seção, campos e rótulos acompanham o idioma da prosa, sem misturar idiomas no mesmo artefato novo. Ao editar um artefato existente, mantenha o idioma da prosa e o dos títulos que ele já usa, mesmo que um difira do outro: não traduza um documento sem pedido.

Esta skill nomeia títulos e rótulos em português. Num artefato em inglês, use a coluna English da tabela abaixo; em outro idioma, traduza a coluna Português e use a mesma tradução em todos os artefatos da pasta, para que documentos diferentes usem os mesmos nomes.

Nomes de APIs, tipos, paths e identificadores não se traduzem, nem termos canônicos como capability, JTBD, MoSCoW (Must, Should, Could, Won't), NFR, EARS, trade-off, Leading, Lagging, Guardrails e Gate. Outros termos técnicos estabelecidos podem ficar em inglês quando a tradução perder precisão. A permissão vale para termos, não para expressões: em vez de escrever `if false` no meio da prosa, descreva a condição e o seu impacto.

| Artefato | Português | English |
| --- | --- | --- |
| PRD, spec e design | Premissas, Lacunas | Assumptions, Gaps |
| Spec e design | Campo `Confirmada?` com `s` ou `n` | Field `Confirmed?` with `y` or `n` |
| PRD | Resumo executivo, Alinhamento estratégico, Contexto e problema, Usuário-alvo / JTBD, Oportunidade / hipótese, Solução proposta, Glossário do domínio, Requisitos funcionais, Eventos de domínio, Requisitos não funcionais, Considerações regulatórias, Fora do escopo, Trade-offs declarados, Métricas de sucesso, Critérios de aceitação, Dependências e riscos, Ponto mais frágil, Referências; Prefixo dos requisitos, Capabilities afetadas, Visão geral, Identificador, `*Custo:*`, `*Motivo:*` | Executive Summary, Strategic Alignment, Context and Problem, Target User / JTBD, Opportunity / Hypothesis, Proposed Solution, Domain Glossary, Functional Requirements, Domain Events, Non-functional Requirements, Regulatory Considerations, Non-goals, Declared Trade-offs, Success Metrics, Acceptance Criteria, Dependencies and Risks, Weakest Point, References; Requirement Prefix, Affected Capabilities, Overview, Identifier, `*Cost:*`, `*Reason:*` |
| Visão geral de produto | Escopo, Propósito, Capabilities, Catálogo de eventos, Fluxos entre capabilities, Termos com mais de um significado, Decisões delegadas a ADR | Scope, Purpose, Capabilities, Event Catalog, Flows Between Capabilities, Terms with Multiple Meanings, Decisions Delegated to ADR |
| Spec | Prefixo dos requisitos, PRD de origem, Contexto, Escopo / Fora do escopo, Requisitos, Decisões observáveis, Eventos de domínio, Glossário, Rastreabilidade, Divergências, `Retirados:` | Requirement Prefix, Source PRD, Context, Scope / Out of Scope, Requirements, Observable, Domain Events, Glossary, Traceability, Divergences, `Retired:` |
| Design | Contexto do design, Critérios de avaliação, Riscos e técnicas, Abordagens, Visão da arquitetura, Unidade de implantação, Componentes, Eventos de domínio, Modelo de dados, Tratamento de erros, Decisões técnicas, Arquivos a criar ou alterar | Design Context, Evaluation Criteria, Risks and Techniques, Approaches, Architecture Overview, Deployment Unit, Components, Domain Events, Data Model, Error Handling, Technical Decisions, Files to Create or Modify |
| Tarefas | Comandos de gate, Plano de execução, Tarefas, Rastreabilidade, Desvios, Tarefas de correção; campos O quê, Onde, Depende de (`nenhuma`), Requisitos, Interfaces, Pronto quando, Testes, Gate | Gate Commands, Execution Plan, Tasks, Traceability, Deviations, Correction Tasks; fields What, Where, Depends on (`none`), Requirement, Interfaces, Done when, Tests, Gate |
| ADR | `ADR NNNN: decisão`, Participantes, Contexto, Decisão, Alternativas consideradas, Consequências, Regras derivadas, `Substitui: NNNN`, `Substituído por: NNNN` | `ADR NNNN: decision`, Participants, Context, Decision, Alternatives considered, Consequences, Derived rules, `Supersedes: NNNN`, `Superseded by: NNNN` |
