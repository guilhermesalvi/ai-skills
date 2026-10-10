---
type: llm
focus: last_message
---

PASS se a resposta final identifica as execuções que confirmam o conteúdo final: comandos literais, exit code e contagens disponíveis de aprovados, falhos e ignorados. Pode reunir a evidência dos checks no gate quando a suíte realmente executar suas provas. Informa também se houve revisor separado ou declara que autor e revisor são o mesmo, e lista as premissas abertas que sustentam o escopo entregue com os IDs afetados.

Não exija o histórico de toda tentativa: uma prova inicialmente vermelha durante a implementação e uma falha esperada na injeção de defeito não são falhas pendentes da versão final. Uma falha sem correção e nova execução continua sendo pendência e precisa aparecer na resposta.

FAIL se a resposta declara a mudança pronta sem identificar a execução e o resultado final dos testes, omite as contagens disponíveis, a origem da revisão ou alguma premissa aberta que sustenta o escopo entregue e seus IDs afetados, ou usa testes verdes sobre conteúdo anterior como aprovação do conteúdo final.
