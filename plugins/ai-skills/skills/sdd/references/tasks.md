# Decomposição em tarefas

Produza um plano que outro executor consiga seguir sem adivinhar comportamento ou dependências. Cada tarefa entrega uma mudança coesa, com implementação, integração e verificação pertinentes.

## Conhecer a verificação do projeto

Leia as instruções das áreas atingidas, a documentação de build e testes, a configuração dos projetos e a CI. Inspecione testes pertinentes para entender framework, estilo e camada, sem impor uma amostra fixa ou copiar todos os níveis de teste para qualquer tarefa.

Registre no plano o estado inicial dos checks quando ele for necessário para distinguir regressões; uma contagem histórica não substitui os resultados dos testes.

Escolha a verificação que observa o requisito. Testes de domínio, integração, publicação ou mutação entram quando a mudança, a regra local ou o pedido os justifica. Uma ausência de ferramenta é uma limitação a resolver ou reportar, sem declarar sucesso fictício.

## Unidade de trabalho

Uma tarefa tem um resultado integrável: por exemplo, operação com validação, registro no módulo e testes correspondentes. Divida resultados independentes. Se os testes só puderem executar após uma dependência, ajuste o agrupamento para entregar algo verificável.

| Campo | Conteúdo |
| --- | --- |
| What | Resultado concreto da tarefa |
| Where | Caminhos já determinados, distinguindo criação e alteração; colocação ainda em aberto fica com o executor |
| Depends on | IDs das dependências ou `none` |
| Requirement | Requisitos satisfeitos ou preservados |
| Interfaces | Contratos consumidos e produzidos, com tipos e erros pertinentes |
| Done when | Critérios observáveis e binários, incluindo a verificação a executar |
| Tests | Casos e nível necessário, ou motivo para não adicionar testes |
| Gate | Comando ou referência inequívoca aos checks aplicáveis |

Preserve esses campos quando usar o formato da skill. O texto de Interfaces deve ser suficiente para entender a tarefa, e os links para spec e design permitem conferir o contrato completo. Não invente uma interface ausente nem use "similar à tarefa anterior" como especificação.

O critério de conclusão aponta o teste que decide o requisito, não a suíte que passou: uma suíte verde não resolve nenhuma obrigação individual. Quando um requisito quantifica sobre um conjunto, cada membro nomeado na spec precisa de caso, ou de um caso que percorra o conjunto inteiro com o tamanho declarado.

## Ordem e rastreabilidade

Ordene por dependência, sem ciclos ou referência a uma tarefa inexistente. Agrupe por coesão; fases fixas de fundação, domínio e adapters não são obrigatórias. Cada requisito em escopo deve ter um caminho até implementação e evidência. Não atribua à tarefa um requisito que ela não verifica.

O documento pode conter Gate Commands, Execution Plan, Tasks e Traceability; acrescente Deviations ou Correction Tasks quando houver conteúdo. Se não houver design separado, explique a estrutura necessária no início das tarefas.

A tabela de comandos usa os checks pertinentes, como `quick`, `full` e `build`, se esses nomes ajudarem. A última tarefa de uma fase não exige repetir toda a suíte quando já existe evidência válida para o mesmo estado. Uma mudança posterior ou falha justifica a repetição dos checks afetados.

## Exemplo parcial

Exemplo de formato, com tipos e requisitos fictícios.

```markdown
### T1: Implementar criação idempotente de solicitações

- **What:** criar solicitação uma única vez para uma chave e conteúdo iguais
- **Where:** criar `src/Example/Requests/RequestService.cs` e os testes correspondentes
- **Depends on:** none
- **Requirement:** EXM-01, EXM-02
- **Interfaces:** consome `CreateRequest` e armazenamento por chave; produz `CreateResult` com solicitação ou conflito
- **Done when:**
  - [ ] Repetir chave e conteúdo retorna o resultado original sem duplicar (EXM-01)
  - [ ] Repetir a chave com outro conteúdo informa conflito e preserva a primeira solicitação (EXM-02)
  - [ ] Os testes pertinentes passam
- **Tests:** casos de criação, repetição equivalente e conflito
- **Gate:** comando de testes confirmado na configuração da mudança
```

Na tarefa real, substitua a indicação de comando por um comando executável confirmado.
