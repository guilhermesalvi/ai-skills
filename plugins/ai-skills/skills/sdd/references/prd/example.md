# Exemplo de PRD

Um PRD de capability, sem PRD 0000. Ele não tem Considerações regulatórias, para não apresentar alegações regulatórias como fatos verificados.

````markdown
# Verificação assíncrona de documentos

| | |
| --- | --- |
| **Prefixo dos requisitos** | `DOC` |
| **Capabilities afetadas** | Ativação de conta |

## Resumo executivo

A operação precisa acompanhar documentos enviados para análise sem coordenar cada envio por e-mail. A proposta mantém um caso de verificação por cliente, com estado explícito e critérios para cada item. A elegibilidade para ativação depende do resultado do caso. A proposta parte da hipótese, ainda não medida, de que a espera entre envios e análises é o principal componente do prazo atual.

## Contexto e problema

Neste cenário fictício, a operação envia documentos em nome do cliente e acompanha a análise por mensagens. A aprovação não tem um registro único que os consumidores possam consultar. Não há baseline medido para estabelecer a meta de prazo.

## Usuário-alvo / JTBD

- Analista de conformidade: validar cada documento contra um critério identificável e registrar o resultado.
- Operador de cadastro: saber o estado do caso e quais itens exigem reenvio.
- Ativação de conta: consultar a elegibilidade do cliente sem interpretar mensagens.

## Solução proposta

Um caso reúne os itens exigidos para o cliente e informa o resultado da verificação. A operação envia documentos; a análise aprova itens ou informa o motivo de rejeição. Os requisitos abaixo definem as transições.

```mermaid
stateDiagram-v2
    [*] --> AwaitingDocuments: convite (DOC-01)
    AwaitingDocuments --> UnderReview: envio completo (DOC-03)
    UnderReview --> Approved: aprovação (DOC-07)
    UnderReview --> PendingResubmission: rejeição de item (DOC-06)
    PendingResubmission --> UnderReview: reenvio (DOC-08)
    UnderReview --> Declined: recusa (DOC-09)
    PendingResubmission --> Declined: prazo excedido (DOC-10)
```

| Estado | Identificador | Significado |
| --- | --- | --- |
| Aguardando documentos | `AwaitingDocuments` | Convite ativo com envio incompleto |
| Em análise | `UnderReview` | Caso disponível para análise |
| Aguardando reenvio | `PendingResubmission` | Há item rejeitado |
| Aprovado | `Approved` | Resultado terminal que permite ativação |
| Recusado | `Declined` | Resultado terminal de recusa ou expiração |

Armazenamento, notificações e desenho da interface serão definidos no trabalho técnico.

## Glossário do domínio

| Termo | Definição |
| --- | --- |
| Caso de verificação | Itens exigidos de um cliente e seu estado de análise |
| Item | Documento com resultado próprio: pendente, aprovado ou rejeitado |
| Checklist | Critérios por tipo de cliente, com versão escolhida no convite (DOC-05) |
| Envio completo | Todos os itens do checklist têm documento anexado (DOC-03) |
| Elegibilidade | Resultado derivado do estado do caso (DOC-11) |

## Requisitos funcionais

- **DOC-01 (Must)** O caso começa em `AwaitingDocuments` a partir de um convite ativo.
- **DOC-02 (Must)** O operador pode enviar documentos em nome do cliente enquanto o convite estiver ativo, independentemente da disponibilidade do analista.
- **DOC-03 (Must)** O caso passa a `UnderReview` quando todos os itens exigidos têm documento anexado.
- **DOC-04 (Must)** O sistema rejeita imediatamente um item com formato ou tamanho incompatível com o checklist e informa o critério violado.
- **DOC-05 (Must)** A conformidade define e versiona o checklist por tipo de cliente; o caso usa a versão vigente no convite.
- **DOC-06 (Must)** Rejeitar um item exige um motivo previsto no checklist e leva o caso a `PendingResubmission`.
- **DOC-07 (Must)** Aprovar todos os itens leva o caso a `Approved`, que é terminal.
- **DOC-08 (Must)** Em `PendingResubmission`, somente itens rejeitados aceitam reenvio; um reenvio leva o caso a `UnderReview`, preservando os resultados dos demais itens.
- **DOC-09 (Must)** A conformidade pode recusar um caso em `UnderReview` com motivo registrado; `Declined` é terminal.
- **DOC-10 (Must)** Um caso em `PendingResubmission` há mais de 10 dias úteis passa a `Declined` com motivo de prazo excedido.
- **DOC-11 (Must)** A elegibilidade para ativação é verdadeira se, e somente se, o caso estiver em `Approved`.
- **DOC-12 (Must)** Cada envio, validação e transição registra responsável, instante e motivo, consultáveis por caso e cliente.

## Requisitos não funcionais

- **DOC-13 (Must)** Um envio completo deve ser refletido em `UnderReview` em até 1 minuto.
- **DOC-14 (Must)** Traces não contêm documentos nem dados pessoais; identificadores técnicos de caso e item são suficientes.

## Fora do escopo

- Envio direto pelo cliente nesta versão.
- Assinatura de contratos.
- Revisão do mérito dos critérios de conformidade.

## Trade-offs declarados

### Operação intermediando o envio (DOC-02)

*Custo:* mantém parte da carga manual.

*Motivo:* permite avaliar o fluxo interno antes de abrir o envio ao cliente.

### Checklist atual preservado (DOC-05)

*Custo:* critérios legados de pouco valor podem continuar no processo.

*Motivo:* rever seu mérito exige uma decisão de produto distinta.

### Prazo de reenvio de 10 dias úteis (DOC-10)

*Custo:* clientes mais lentos precisam de novo convite.

*Motivo:* limita casos pendentes por tempo indefinido.

## Métricas de sucesso

### Leading

- Taxa de reenvio por formato ou tamanho inválido (DOC-04): medir se o feedback no envio reduz retrabalho.

### Lagging

- Prazo entre envio completo e resultado terminal: medir baseline e distribuição antes de definir a meta.

### Guardrails

- Taxa de erros encontrados após a aprovação: a redução de prazo não pode comprometer a análise.

## Critérios de aceitação

| Caso | Entrada | Condição intermediária | Requisito | Resultado |
| --- | --- | --- | --- | --- |
| Envio completo | Três itens válidos anexados às 10h | Checklist completo | DOC-03, DOC-13 | `UnderReview` até 10h01 |
| Formato inválido | Item 2 em formato não aceito | Critério de formato violado | DOC-04 | Item rejeitado com motivo; sem completar o checklist |
| Rejeição parcial | Itens 1 e 3 aprovados, item 2 rejeitado | Motivo registrado | DOC-06, DOC-08 | `PendingResubmission`; somente item 2 pode ser reenviado |
| Reenvio parcial | Itens 2 e 3 rejeitados; somente 2 reenviado | Item 3 ainda rejeitado | DOC-08 | `UnderReview`, preservando a rejeição do item 3 |
| Aprovação | Três itens aprovados | Nenhum item pendente | DOC-07, DOC-11 | `Approved`; elegibilidade verdadeira |
| Prazo excedido | Caso pendente por 11 dias úteis | Sem reenvio | DOC-10, DOC-11 | `Declined`; elegibilidade falsa |

## Dependências e riscos

| Item | Tipo | Impacto |
| --- | --- | --- |
| Definição e versão do checklist | Dependência de produto | Sem critérios, a análise não pode começar |
| Ativação de conta | Capability consumidora | Precisa interpretar a elegibilidade conforme DOC-11 |

## Premissas

### O principal atraso está na espera entre envios e análise

**Premissa:** o tempo de espera, e não o de análise, domina o prazo atual.

**Evidência:** relatos da operação sobre documentos parados à espera de análise; não há medição.

**Impacto:** se a premissa for falsa, digitalizar o fluxo reduz pouco o prazo e a proposta perde sua justificativa.

**Responsável:** operação.

**Verificação:** medir os tempos de espera e de análise em casos reais antes de aprovar.

## Lacunas

### Calendário de dias úteis

**Decisão pendente:** qual calendário define os dias úteis da expiração.

**IDs afetados:** DOC-10.

**Impacto:** determina quando um caso pendente passa a `Declined`.

**Responsável:** autor do produto.

### Retenção de documentos

**Decisão pendente:** quais política e obrigações definem a retenção.

**Impacto:** sem ela, o PRD não define por quanto tempo os documentos são mantidos nem quando são descartados; o requisito será escrito quando a decisão existir.

**Responsável:** conformidade.

### Limite do guardrail de erros

**Decisão pendente:** a taxa máxima de erros encontrados após a aprovação.

**Impacto:** sem limite, o guardrail não indica quando a redução de prazo passa a comprometer a análise.

**Responsável:** conformidade.

## Ponto mais frágil

**Decisão:** preservar o checklist atual sem revisar o mérito dos critérios (DOC-05).

**Risco:** exigências legadas podem continuar causando retrabalho sem melhorar a análise.

**Mitigação:** medir os motivos de reenvio desde o início do fluxo.

**Critério de reavaliação:** se a maior parte do retrabalho decorrer do mérito dos critérios, a decisão de adiar sua revisão precisa ser reavaliada.
````

## Exemplo de edição

**Antes:** “Deverá ser realizada a rejeição do item e a disponibilização da informação sobre o critério que foi violado.”

**Depois:** “O sistema rejeita o item e informa o critério violado.”

A edição troca a forma e preserva o resultado. Condições, instante e limites continuam definidos no requisito completo; a frase isolada não os substitui.
