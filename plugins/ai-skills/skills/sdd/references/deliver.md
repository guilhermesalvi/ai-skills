# Entrega

Confira os artefatos e prepare uma resposta que mostre o resultado, a prova e as decisões ainda abertas.

## Conferência final

O `check_spec.py` não julga conteúdo. Antes de responder, confira os itens aplicáveis aos artefatos e à resposta final; corrija o texto quando um falhar:

- [ ] A spec leva o nome da capability, não o da funcionalidade pedida.
- [ ] A prosa, inclusive as palavras-chave EARS, está no idioma do pedido ou da convenção.
- [ ] Cada decisão cujo erro custaria dinheiro, dado, conformidade ou um contrato publicado está em Gaps, e o comportamento provisório dela está identificado como escolha provisória em Assumptions.
- [ ] Nenhuma dimensão que se aplica ficou na linha `n/a`.
- [ ] Assumptions contém apenas premissas abertas; fatos verificados e escolhas decididas foram registrados no corpo com evidência ou origem, e as citações afetadas foram atualizadas.
- [ ] A resposta foi comparada com Assumptions da spec e do plano: cada premissa ainda aberta que sustenta o escopo entregue está na resposta com os IDs afetados.
- [ ] Os checks provam o que a spec exige, não o que o código já faz.
- [ ] Cada seção opcional presente acrescenta informação necessária; nenhuma apenas declara ausência nem repete outra seção.

## Resposta

Inclua também as conferências não feitas, como o `check_spec.py` ou o `git log -S`, com o motivo.

Citar uma lacuna ou recomendar um default não solicita a decisão do usuário. Formule as perguntas exigidas pelo contrato de entrega do `SKILL.md`.

Motivo: sem aprovações intermediárias, um default de negócio só apareceria para quem abrisse o artefato.

### Exemplo parcial de resposta

Use este exemplo para reconhecer os registros de entrega; derive o conteúdo dos artefatos atuais:

> Spec e plano criados em `docs/specs/invoice-issuance/`; validador sem achados.
>
> Escolha provisória: emissão recusada enquanto faltar a política de arredondamento (INV-04). A política está em Gaps; a recusa é provisória.
>
> Qual regra de arredondamento deve valer: por item ou pelo total da fatura? Recomendo seguir a regra contábil confirmada pelo responsável financeiro.

## Implementação e verificação

Comece pelo resultado e pela cobertura conhecida. Inclua estes registros na resposta final, além das pendências acima:

| Registro | Evidência a apresentar |
| --- | --- |
| Checks executados | Comando literal, exit code e contagens disponíveis de aprovados, falhos e ignorados; a contagem sozinha não identifica a execução |
| Revisão | Revisor separado, quando houver; caso contrário, declare que autor e revisor são o mesmo |
| Injeção de falha | Resultado e escopo numa mudança não trivial; se não foi executada, motivo e impacto |
| Achados | Ordem de impacto, ressalvas do plano e ação necessária para resolver |

Distinga observação, hipótese e verificação não executada. Não transforme inspeção estática em prova de runtime, nem uma nota de confiança em aprovação do produto.
