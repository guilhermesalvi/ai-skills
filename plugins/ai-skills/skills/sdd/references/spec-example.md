# Exemplo de spec

Use este exemplo para reconhecer um comportamento completo: da solicitação de cancelamento à confirmação ou recusa observável. O cenário e as evidências são fictícios; use as fontes do projeto nos artefatos reais.

- O recorte inclui efeitos e recusas necessários ao cancelamento, sem reconstruir pagamento, envio ou entrega.
- Assumptions registra uma escolha provisória que atende uma lacuna; a decisão continua aberta.
- As garantias existentes do chamador estão em Context. Mapas de decisões, dimensões inaplicáveis e seções sem informação adicional foram omitidos.

````markdown
# Cancelamento de pedido

| | |
| --- | --- |
| **Requirement Prefix** | `CAN` |

## Context

O cliente solicita o cancelamento de um pedido e precisa receber a confirmação, ou distinguir a recusa por propriedade ou estado. O resultado encerra o fluxo quando o cliente conhece a resposta e o estado final do pedido.

O contrato vem do pedido do produto: o dono pode cancelar um pedido ainda não pago. A classe fictícia `Order`, em `orders/orders.py`, mantém estado e histórico; `Order.pay` só cobra em `PENDING`. Este recorte usa esses contratos existentes sem redefinir pagamento, envio ou entrega.

O chamador entrega identidade autenticada, conforme `current_customer` em `api/session.py`, e serializa operações do mesmo pedido com `order_lock`, em `api/orders.py`.

## Assumptions

- **Recusa provisória de pedido pago.** Enquanto a lacuna Política de cancelamento de pedido pago não tiver decisão, CAN-03 recusa o cancelamento de pedido em `PAID` e preserva pedido e cobrança. Se o produto permitir cancelar pedidos pagos, a recusa precisará mudar.

## Gaps

| Gap | Affects | Owner |
| --- | --- | --- |
| Política de cancelamento de pedido pago | CAN-03, caso `PAID` | Produto |

## Requirements

- **CAN-01** — QUANDO o dono solicitar o cancelamento de um pedido em `PENDING`, ENTÃO o sistema DEVE confirmar o cancelamento, deixar o pedido em `CANCELLED` e acrescentar ao histórico o estado final e o instante UTC.
- **CAN-02** — SE outro cliente solicitar o cancelamento, ENTÃO o sistema DEVE recusar com erro de propriedade distinto de erro de estado e preservar o pedido.
- **CAN-03** — SE o dono solicitar o cancelamento de um pedido em `PAID`, `SHIPPED` ou `DELIVERED`, ENTÃO o sistema DEVE recusar com erro de estado e preservar o pedido.
- **CAN-04** — QUANDO o dono repetir o cancelamento de um pedido em `CANCELLED`, ENTÃO o sistema DEVE confirmar o estado vigente sem acrescentar outro registro ao histórico.
- **CAN-05** — O cancelamento NÃO DEVE gerar cobrança; a tentativa de pagar um pedido já cancelado DEVE ser recusada antes da cobrança pela guarda de estado de `Order.pay`, em `orders/orders.py`.

````
