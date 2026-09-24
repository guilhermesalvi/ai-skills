# Orientações do repositório

Este repositório distribui as skills `sdd` e `transcript-fix` no plugin `ai-skills` do Claude Code. O pacote fica em `plugins/ai-skills/`, com o manifesto em `plugins/ai-skills/.claude-plugin/plugin.json`, e o marketplace em `.claude-plugin/marketplace.json`. Instruções, referências e textos de interface das skills ficam em português. Código, identificadores, comentários, mensagens dos scripts e commits ficam em inglês. Títulos de seção, rótulos, tags e campos dos artefatos que as skills geram acompanham o idioma da prosa do artefato; cada skill documenta os nomes em português e mantém uma única tabela de equivalência com o inglês. Termos canônicos em inglês, como JTBD, MoSCoW, NFR, trade-off, Leading, Lagging e Guardrails, não se traduzem.

## Editar as skills

- Mantenha no `SKILL.md` o escopo, as entradas, os limites e os links para as referências. Procedimentos condicionais ficam em `references/`, e operações determinísticas, em `scripts/`.
- O `description` do frontmatter decide quando o Claude Code carrega a skill: diga o que ela faz, quando usar e quando não usar. Preserve o `name`, que nomeia a invocação `/ai-skills:<skill>`, e não desabilite a invocação pelo modelo.
- Resolva scripts e referências a partir da pasta do `SKILL.md` carregado. Nos exemplos, `<skill-dir>` representa esse caminho absoluto; não é uma variável fornecida pelo Claude Code. Mantenha caminhos dos dados relativos ao projeto consumidor, sem mudar o diretório de trabalho para a instalação da skill.
- Escreva instruções imperativas e diretas, com o motivo das restrições que não são óbvias. Descreva o resultado e os critérios de aceitação em vez do raciocínio passo a passo; use passos numerados só onde a ordem importa. Não use ênfase em caixa alta, limites numéricos de tamanho de saída, contagens fixas de rodadas nem limiares numéricos sem fundamento, exceto em contratos que um script confere.
- Trate um assunto por parágrafo. Uma instrução condicional diz quando agir, que ação tomar e que resultado produzir; a exceção fica junto da regra ou cita o arquivo e a seção que a definem.
- Cada regra tem uma única fonte. Não repita nem cite regra que já está em contexto: o `SKILL.md` é carregado antes de suas referências; as instruções `CLAUDE.md` e `CLAUDE.local.md` do consumidor seguem o escopo de diretório do Claude Code. Cite outra fonte só quando o leitor precisar lê-la para agir, e prefira o nome estável (arquivo, seção, tag ou rótulo) a link com âncora de seção.
- Não crie links entre skills, porque cada uma pode ser copiada sozinha.
- Mantenha as skills genéricas. Regra de um projeto consumidor fica no `CLAUDE.md` dele, e as skills a aplicam pela precedência do pedido e da convenção do repositório sobre seus defaults.
- Siga o escopo e a autorização do usuário. Não acrescente aprovações para escolhas rotineiras, edições ou validações já autorizadas.
- Não fixe modelos nas skills, nem por ID, nem por alias, nem por classificação estática. A `transcript-fix` escolhe o modelo dos subagentes durante a execução.
- Ao mudar a orquestração da `transcript-fix`, preserve as saídas exclusivas por executor, o glossário imutável por etapa e a divisão e reunião determinísticas dos trechos.

## Validar

Os scripts usam Python 3.10+ e só a biblioteca padrão. Depois de mudar o comportamento deles, rode:

```bash
python -m unittest discover -s tests -v
```

Depois de mudar instruções ou empacotamento, confira o frontmatter, os links relativos e os caminhos dos manifestos com os validadores da CLI:

```bash
claude plugin validate . --strict
claude plugin validate plugins/ai-skills --strict
claude plugin validate plugins/ai-skills/skills --strict
```

Siga o teste de instalação isolada do README para verificar o pacote ponta a ponta. Quando disponível, use também a skill `skill-creator`. Não crie testes que apenas repetem o texto dos prompts.

## Commits

Mensagens seguem `<type>: <description>`, em inglês, com até 60 caracteres, descrição no imperativo e inicial minúscula. Tipos: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `style`, `revert`. Sem escopo, ponto final, `!`, corpo ou trailers.

Agrupe por motivo: skill, scripts e testes da mesma mudança ficam no mesmo commit; motivos independentes, em commits separados. Faça commit e push só com autorização do usuário.
