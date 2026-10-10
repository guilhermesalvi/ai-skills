# Entrega

Confira os artefatos e prepare uma resposta que mostre o resultado, a prova e as decisões ainda abertas.

## Conferência final

O `check_spec.py` não julga conteúdo. Antes de responder, confira os itens aplicáveis aos artefatos e à resposta final; corrija o texto quando um falhar:

- [ ] Uma spec nova descreve o menor comportamento completo, com gatilho e resultado para o consumidor; contratos existentes não foram duplicados nem fragmentados por tarefa.
- [ ] As regras novas têm origem identificável ou estão registradas como escolhas provisórias. As condições ainda não confirmadas necessárias para garantir o resultado estão na spec, mesmo quando o mecanismo que as atende pertence ao plano.
- [ ] A prosa, inclusive as palavras-chave EARS, está no idioma do pedido ou da convenção.
- [ ] Cada decisão ainda ausente cujo erro custaria dinheiro, dado, conformidade ou um contrato publicado está em Gaps; quando houver comportamento provisório seguro, ele está identificado como escolha provisória em Assumptions.
- [ ] Em Observable Decisions, quando presente, nenhuma dimensão que se aplica ficou na linha `n/a`.
- [ ] Assumptions contém apenas premissas abertas; fatos verificados e escolhas decididas foram registrados no corpo com evidência ou origem, e as citações afetadas foram atualizadas.
- [ ] Depois dos últimos ajustes, Assumptions foi relida nos arquivos atuais da spec e do plano, e a resposta traz as premissas abertas conforme Resposta.
- [ ] Os checks provam o que a spec exige, não o que o código já faz.
- [ ] Cada seção opcional presente acrescenta informação necessária; nenhuma apenas declara ausência nem repete outra seção.
- [ ] Execution, quando presente, permite localizar contexto, dependências e provas de cada item; a integração foi verificada sobre o escopo completo, ou sua pendência e impacto estão na entrega.

## Resposta

Inclua na própria resposta final:

- Os caminhos dos artefatos, o resultado e as evidências.
- Percorra Assumptions da spec e do plano e inclua cada premissa ainda aberta que sustenta a entrega. Ao lado de cada uma, cite os IDs dependentes; para uma premissa apenas técnica, cite o nome da decisão em Technical Decisions ou do check afetado, como aparece no plano. Uma descrição genérica da área não localiza essa dependência.
- Perguntas diretas sobre as lacunas de negócio abertas: nomeie as alternativas concretas que o usuário pode escolher e indique a recomendação. Uma pergunta de sim ou não sem alternativas nomeadas não apresenta essas opções.
- As conferências não feitas, como o `check_spec.py` ou o `git log -S`, com o motivo.

Citar uma lacuna ou recomendar um default não solicita a decisão do usuário. Escreva a pergunta sobre a escolha que falta.

Motivo: sem aprovações intermediárias, um default de negócio só apareceria para quem abrisse o artefato.

### Exemplo parcial de resposta

Use este exemplo para reconhecer os registros de entrega; derive o conteúdo dos artefatos atuais:

> Spec e plano criados em `docs/specs/invoice-issuance/`; validador sem achados.
>
> Escolha provisória: emissão recusada enquanto faltar a política de arredondamento (INV-04). A política está em Gaps; a recusa é provisória.
>
> Qual regra de arredondamento deve valer: por item ou pelo total da fatura? Recomendo por item, para que o total coincida com a soma dos valores exibidos. A escolha ainda precisa da decisão do responsável financeiro.

## Implementação e verificação

Comece pelo resultado e pela cobertura conhecida. Inclua estes registros na resposta final, além das pendências acima:

| Registro | Evidência a apresentar |
| --- | --- |
| Checks executados | Comando literal e resultado sobre o conteúdo final: exit code e contagens disponíveis de aprovados, falhos e ignorados, inclusive zero; a contagem sozinha não identifica a execução |
| Revisão | Revisor separado, quando houver; caso contrário, declare que autor e revisor são o mesmo |
| Injeção de falha | Resultado e escopo numa mudança não trivial; se não foi executada, motivo e impacto |
| Achados | Ordem de impacto, ressalvas do plano e ação necessária para resolver |

Distinga observação, hipótese e verificação não executada. Não transforme inspeção estática em prova de runtime, nem uma nota de confiança em aprovação do produto.
