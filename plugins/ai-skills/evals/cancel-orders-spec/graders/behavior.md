---
type: llm
focus: { source: file, path: eval-out/spec.md }
---

PASS se a spec tem como contrato o cancelamento de pedido, da solicitação do cliente ao resultado de confirmação ou recusa e ao estado final. Inclui as regras de propriedade, repetição, estados que aceitam ou recusam e a relação com pagamento que afetam esse resultado. Pode usar premissas ou lacunas explícitas quando a fonte não decidir autorização ou concorrência.

FAIL se a spec reconstrói gestão de pedidos, pagamento, envio e entrega como requisitos independentes sem necessidade para o cancelamento, ou se descreve apenas um endpoint, uma camada ou uma tarefa sem o resultado completo. Cite evidência para distinguir uma dependência pertinente da ampliação desnecessária do domínio. Avalie também se a proteção contra pagamento concorrente foi decidida, registrada como premissa verificável ou mantida como lacuna com impacto claro.
