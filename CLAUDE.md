# Orientações do repositório

Este repositório distribui a skill `sdd` no plugin `ai-skills` do Claude Code. O pacote fica em `plugins/ai-skills/`, com o manifesto em `plugins/ai-skills/.claude-plugin/plugin.json`, e o marketplace em `.claude-plugin/marketplace.json`. Instruções, referências e textos de interface das skills ficam em português. Código, identificadores, comentários, mensagens dos scripts e commits ficam em inglês. Títulos de seção, rótulos, colunas e campos dos artefatos que as skills geram formam um schema em inglês, independente do idioma da prosa, e cada nome é definido uma só vez, na referência do artefato. Termos canônicos em inglês, como EARS, NFR e trade-off, não se traduzem.

## Editar as skills

- Mantenha no `SKILL.md` o escopo, as entradas, os limites e os links para as referências. Procedimentos condicionais ficam em `references/`, operações determinísticas, em `scripts/`, e modelos dos artefatos, em `assets/`.
- Uma regra que um script consegue conferir vira conferência do script, e a referência diz apenas quando executá-lo e o que ele não cobre.
- O `description` do frontmatter decide quando o Claude Code carrega a skill: diga o que ela faz, quando usar e quando não usar. Preserve o `name`, que nomeia a invocação `/ai-skills:<skill>`, e não desabilite a invocação pelo modelo.
- Resolva scripts e referências a partir da pasta do `SKILL.md` carregado. Nos exemplos, `<skill-dir>` representa esse caminho absoluto; não é uma variável fornecida pelo Claude Code. Mantenha caminhos dos dados relativos ao projeto consumidor, sem mudar o diretório de trabalho para a instalação da skill.
- Escreva instruções imperativas e diretas, com o motivo das restrições que não são óbvias. Descreva o resultado e os critérios de aceitação em vez do raciocínio passo a passo; use passos numerados só onde a ordem importa. Não use ênfase em caixa alta, limites numéricos de tamanho de saída, contagens fixas de rodadas nem limiares numéricos sem fundamento, exceto em contratos que um script confere.
- Estruture cada referência como Markdown navegável: um título por assunto que o leitor procura, cada regra num item de lista próprio, tabelas para escolhas entre casos e parágrafo só para um contexto curto. Duas regras não dividem a mesma frase, para que nenhuma fique escondida no meio de outra.
- Uma instrução condicional diz quando agir, que ação tomar e que resultado produzir; a exceção fica no item seguinte ao da regra ou cita o arquivo e a seção que a definem.
- Numa referência com mais de 100 linhas, abra com uma linha `Conteúdo:` que liste os títulos, como recomenda o guia de skills da Anthropic: uma leitura parcial ainda mostra o que o arquivo cobre.
- Não use metáforas nem termos cunhados; um termo usado em mais de uma referência é definido no `SKILL.md`.
- Cada regra tem uma única fonte. A exceção é a conferência final da entrega, no fluxo comum, que nomeia em uma linha as regras de julgamento que nenhum script confere, porque é ali que o agente as aplica. Fora dela, não repita nem cite regra que já está em contexto: o `SKILL.md` é carregado antes de suas referências; as instruções `CLAUDE.md` e `CLAUDE.local.md` do consumidor seguem o escopo de diretório do Claude Code. Cite outra fonte só quando o leitor precisar lê-la para agir, e prefira o nome estável (arquivo, seção, tag ou rótulo) a link com âncora de seção.
- O critério para ler uma referência fica em quem encaminha para ela, a tabela do `SKILL.md` ou outra referência, porque é aplicado antes da leitura. A referência encaminhada não repete o próprio gatilho: quem a abriu já passou por ele.
- Não crie links entre skills, porque cada uma pode ser copiada sozinha.
- Mantenha as skills genéricas. Regra de um projeto consumidor fica no `CLAUDE.md` dele, e as skills a aplicam pela precedência do pedido e da convenção do repositório sobre seus defaults.
- Siga o escopo e a autorização do usuário. Não acrescente aprovações para escolhas rotineiras, edições ou validações já autorizadas.
- Não fixe modelos nas skills, nem por ID, nem por alias, nem por classificação estática.
- As skills precisam funcionar do Sonnet para cima e em outros agentes que seguem o padrão Agent Skills. O Haiku não é alvo: não acrescente prosa só para compensar limites dele. Regras de forma continuam indo para os scripts, porque ajudam qualquer modelo.

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

Siga o teste de instalação isolada do README para verificar o pacote ponta a ponta. Depois de mudar o comportamento esperado de uma skill, rode as evals descritas no README no Sonnet, o menor modelo suportado, e num modelo maior, e ajuste os casos quando o comportamento esperado mudar. Não crie testes que apenas repetem o texto dos prompts.

## Commits

Mensagens seguem `<type>: <description>`, em inglês, com até 60 caracteres, descrição no imperativo e inicial minúscula. Tipos: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `style`, `revert`. Sem escopo, ponto final, `!`, corpo ou trailers.

Agrupe por motivo: skill, scripts e testes da mesma mudança ficam no mesmo commit; motivos independentes, em commits separados. Faça commit e push só com autorização do usuário.
