# Decomposição em tarefas

Produza um plano que outro executor consiga seguir sem adivinhar comportamento ou dependências. Cada tarefa entrega uma mudança coesa, com implementação, integração e verificação pertinentes.

## Conhecer a verificação do projeto

Leia as instruções das áreas atingidas, a documentação de build e testes, a configuração dos projetos e a CI.

Inspecione os testes pertinentes para entender framework, estilo e camada. Não imponha uma amostra fixa nem copie todos os níveis de teste para qualquer tarefa.

Registre no plano o estado inicial dos checks quando ele for necessário para distinguir regressões. Uma contagem histórica não substitui os resultados dos testes.

Escolha a verificação que observa o requisito. Testes de domínio, integração, publicação ou mutação entram quando a mudança, a regra local ou o pedido os justifica. A ausência de uma ferramenta é uma limitação a resolver ou reportar, nunca motivo para declarar sucesso fictício.

## Unidade de trabalho

Uma tarefa tem um resultado integrável: por exemplo, operação com validação, registro no módulo e testes correspondentes. Divida resultados independentes. Se os testes só puderem executar depois de uma dependência, ajuste o agrupamento para entregar algo verificável.

| Campo | Conteúdo |
| --- | --- |
| O quê | Resultado concreto da tarefa |
| Onde | Caminhos já determinados, distinguindo criação e alteração; colocação ainda em aberto fica com o executor |
| Depende de | IDs das dependências ou `nenhuma` |
| Requisitos | Requisitos satisfeitos ou preservados |
| Interfaces | Contratos consumidos e produzidos, com tipos e erros pertinentes |
| Pronto quando | Critérios observáveis e binários, derivados do resultado dos requisitos, incluindo a verificação a executar |
| Testes | Casos e nível necessário, ou motivo para não adicionar testes |
| Gate | Comando confirmado na configuração real do projeto, ou referência inequívoca aos checks aplicáveis |

O texto de Interfaces precisa ser suficiente para entender a tarefa, e os links para spec e design permitem conferir o contrato completo. Não invente uma interface ausente nem use “similar à tarefa anterior” como especificação.

Pronto quando aponta o teste que decide cada requisito, não a suíte verde. Um requisito sobre um conjunto tem um caso por membro nomeado na spec, ou um caso que percorre o conjunto inteiro com o tamanho declarado.

## Ordem e rastreabilidade

Ordene por dependência, sem ciclos nem referência a uma tarefa inexistente. Agrupe por coesão: fases fixas de fundação, domínio e adapters não são obrigatórias.

Cada requisito em escopo deve ter um caminho até implementação e evidência. Não atribua a uma tarefa um requisito que ela não verifica.

A última tarefa de uma fase não exige repetir toda a suíte quando já existe evidência válida para o mesmo estado; uma mudança posterior ou uma falha justifica repetir os checks afetados.

## Estrutura do documento

Se não houver design separado, explique a estrutura necessária no início das tarefas.

| Seção | Conteúdo |
| --- | --- |
| Comandos de gate | Checks pertinentes, como `quick`, `full` e `build`, se esses nomes ajudarem |
| Plano de execução | Ordem das tarefas por dependência |
| Tarefas | Tarefas com os campos da unidade de trabalho |
| Rastreabilidade | Requisito, tarefa e evidência |
| Desvios | Divergências justificadas do design, quando houver |
| Tarefas de correção | Tarefas de correção vindas da verificação, quando houver |

## Exemplo parcial

```markdown
### T1: Implementar criação idempotente de solicitações

- **O quê:** criar solicitação uma única vez para uma chave e conteúdo iguais
- **Onde:** criar `src/Example/Requests/RequestService.cs` e os testes correspondentes
- **Depende de:** nenhuma
- **Requisitos:** EXM-01, EXM-02
- **Interfaces:** consome `CreateRequest` e armazenamento por chave; produz `CreateResult` com solicitação ou conflito
- **Pronto quando:**
  - [ ] Repetir chave e conteúdo retorna o resultado original sem duplicar (EXM-01)
  - [ ] Repetir a chave com outro conteúdo informa conflito e preserva a primeira solicitação (EXM-02)
  - [ ] Os testes pertinentes passam
- **Testes:** casos de criação, repetição equivalente e conflito
- **Gate:** comando de testes confirmado na configuração da mudança
```
