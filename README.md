# ai-skills

Skills para uso pessoal no Claude Code, empacotadas como plugin.

O pacote está em beta, na versão `0.1.0-beta.3`, definida em [plugin.json](plugins/ai-skills/.claude-plugin/plugin.json). A skill `sdd` acompanha a versão do pacote. Os contratos podem mudar durante o beta, sem compromisso de retrocompatibilidade.

| Skill | Finalidade |
| --- | --- |
| `sdd` | Especificar, planejar, implementar e verificar mudanças com requisitos rastreáveis; registrar decisões em ADRs |

A spec define o menor comportamento completo, do gatilho ao resultado para o consumidor, com suas regras e alternativas. Capability é um agrupamento opcional. O plano registra decisões técnicas, checks com prova e, quando necessário, itens executáveis com contexto e dependências. Modelos e um validador mantêm IDs, links, schema e rastreabilidade coerentes.

Consulte o [guia de uso da sdd](plugins/ai-skills/skills/sdd/README.md) para exemplos de pedidos, entradas e entregas de cada modo.

## Instalação

Na raiz deste checkout:

```bash
claude plugin marketplace add ./
claude plugin install ai-skills@ai-skills
claude plugin list --json
```

Em uma nova sessão, invoque `/ai-skills:sdd`. O Claude Code também carrega a skill quando o pedido corresponde à descrição dela. O pacote não precisa de MCP nem fixa um modelo. `check_spec.py` exige Python 3.10+ e Git.

Para instalar a versão publicada no Git:

```bash
claude plugin marketplace add guilhermesalvi/ai-skills
claude plugin install ai-skills@ai-skills
```

Use uma origem por marketplace. Para trocar entre checkout local e Git, remova o registro anterior com `claude plugin marketplace remove ai-skills` antes de adicionar a nova origem. A origem Git instala a versão publicada; mudanças locais chegam a ela após publicação.

A partir de um checkout, a instalação copia a pasta inteira do plugin, inclusive os resultados de evals em `plugins/ai-skills/evals/results/`, que ficam fora do Git. Apague esses resultados antes de instalar ou grave-os em outro lugar, conforme [Evals](#evals).

### Skill avulsa

Copie a pasta inteira `plugins/ai-skills/skills/sdd` para `.claude/skills/sdd` de um projeto consumidor ou `~/.claude/skills/sdd` para uso pessoal. Invoque com `/sdd`. Escolha o plugin ou a cópia avulsa para não carregar a mesma skill duas vezes.

Os recursos seguem o padrão aberto [Agent Skills](https://agentskills.io/specification). No `SKILL.md`, `${CLAUDE_SKILL_DIR}` é uma substituição do Claude Code; em outro agente, informe o caminho absoluto da pasta da skill.

## Atualização

Incremente o sufixo beta, como de `0.1.0-beta.2` para `0.1.0-beta.3`, ao disponibilizar uma nova revisão para seus projetos. Mantenha a versão em `plugins/ai-skills/.claude-plugin/plugin.json`: o Claude Code fixa a instalação nessa versão e nomeia a cópia em cache por ela. Para atualizar uma instalação:

```bash
claude plugin marketplace update ai-skills
claude plugin update ai-skills@ai-skills
```

Abra uma nova sessão depois de atualizar. Cópias avulsas precisam ser copiadas novamente. Para exercitar uma alteração sem instalar, abra a sessão com `claude --plugin-dir ./plugins/ai-skills`.

## Convenções

- O pedido prevalece sobre os defaults das skills. Aplique `CLAUDE.md`, `CLAUDE.local.md` e `AGENTS.md` pertinentes do consumidor, respeitando o escopo de diretório do Claude Code.
- Instruções e textos de interface ficam em português. A prosa dos artefatos segue o pedido ou a convenção do consumidor; sem definição, segue o idioma do pedido. O schema permanece em inglês.
- As skills continuam o trabalho autorizado até a validação e perguntam sobre decisões ausentes que afetem escopo ou correção. Commit e push exigem autorização do usuário.
- A verificação SDD usa revisor separado sempre que houver subagente disponível, salvo proibição no pedido ou nas instruções; sem ele, informa que autor e revisor são o mesmo. O pacote não escolhe modelos para o usuário.
- Os scripts usam somente a biblioteca padrão. Substitua `<skill-dir>` pela pasta absoluta do `SKILL.md` carregado e execute a partir do projeto consumidor.

## Desenvolvimento

### Escrita e organização

As instruções são imperativas, com entradas e resultados explícitos, e os recursos são lidos de forma progressiva. O entrypoint apresenta propósito e encaminhamento; cada referência detalha uma etapa quando ela for necessária. Consulte a documentação de [skills](https://code.claude.com/docs/en/skills) do Claude Code.

| Conteúdo | Organização |
| --- | --- |
| Contexto, decisão e justificativa | Uma ideia por parágrafo, com evidência pertinente |
| Obrigações e itens paralelos | Bullets com ação e condição claras |
| Comparações e registros com os mesmos campos | Tabelas com cabeçalhos explícitos |
| Dependência real de ordem | Passos numerados |
| Detalhe de uma etapa | Referência indicada no ponto de uso |

EARS, os schemas em inglês, a numeração e os checks rastreáveis são contratos desta skill, não exigências do formato de skills. Mantenha uma fonte por regra e revise instruções conflitantes antes de acrescentar mais orientações.

Os modelos de spec e plano começam pelas partes centrais e pelas pendências. Os blocos opcionais ficam em `assets/spec-sections.md` e `assets/plan-sections.md`; inclua apenas os que acrescentarem informação ao contrato ou à solução.

Assumptions reúne apenas fatos ainda não verificados e escolhas provisórias, numa lista com um parágrafo por premissa: título curto em negrito, usado nas citações, seguido da afirmação, do fundamento e do impacto de estar errada. Ao resolver uma premissa, mova o resultado para o corpo com evidência ou origem da decisão e atualize as referências afetadas. O fluxo completo está em [premissas e lacunas](plugins/ai-skills/skills/sdd/references/workflow.md#premissas-e-lacunas).

### Checks locais

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
claude plugin validate . --strict
claude plugin validate plugins/ai-skills --strict
git diff --check
```

No Windows, `py -3` pode substituir `python`. O validador do repositório confere o catálogo, o manifesto, a versão semântica, o frontmatter e os links dos recursos da skill. Os comandos `claude plugin validate` conferem o marketplace, o manifesto e as skills pelo validador da CLI. Os testes também semeiam cada fixture das evals e executam os testes dela; `resume-contract-conflict` inclui uma regressão local deliberada, que o teste espera ver falhar.

Para verificar a instalação sem modificar sua configuração pessoal:

```bash
python scripts/validate_repo.py --install
```

Esse comando usa um `CLAUDE_CONFIG_DIR` temporário apenas nos processos filhos, registra o checkout, instala o plugin, confere versão e habilitação no inventário e compara os recursos instalados com o pacote. Não precisa de login e apaga o diretório temporário ao terminar. Foi verificado com Claude Code `2.1.270`.

### Evals

Os casos em `plugins/ai-skills/evals/` usam [`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals): cada caso tem `prompt.md`, graders em `graders/` e, quando monta um repositório, `case.yaml` com o scaffold.

| Caso | O que confere |
| --- | --- |
| `cancel-orders-spec` | Comportamento completo com recorte de cancelamento, autorização e concorrência, pedido pago como lacuna, premissas, escopo, concisão e entrega |
| `prepare-dependent-change` | Plano transferível, contexto confirmado, dependências reais, provas da integração, pendência limitada à parte afetada e código intacto |
| `adr-from-code` | ADR derivado do código e histórico, sem inventar participantes, alternativas ou motivos |
| `implement-and-verify` | Implementação, testes nomeados nas provas, execução bem-sucedida, checks marcados e relatório |
| `resume-contract-conflict` | Retomada com diff divergente, preservação da spec e nova execução dos checks afetados |
| `ignores-code-review` | Resposta sobre divisão por zero sem carregar a SDD |

Os scaffolds criam arquivos e repositórios Git como você, fora do sandbox, e só rodam com `--scaffold`. Cada `scaffold.sh` chama `seed.sh`, que executa o `scaffold.py` do caso com Python 3.10+; os mesmos scripts semeiam as fixtures dos testes. No Windows, o scaffold roda no Git Bash, e `seed.sh` restaura `LOCALAPPDATA`, que o harness remove, para que o gerenciador de instalações do Python encontre o interpretador existente.

Os casos escrevem arquivos, então conceda `Write` e `Edit`. `implement-and-verify` e `resume-contract-conflict`, marcados com `needs-bash`, executam testes e precisam de `Bash`. Conceder `Bash` exige o sandbox do sistema, que o Windows nativo não tem: nele, o Claude Code recusa a execução. No Windows nativo, rode os demais casos sem `Bash`:

```bash
claude plugin eval plugins/ai-skills --scaffold --allow-tools Write Edit --tag spec plan adr trigger --no-publish
```

No Linux, no macOS ou no WSL2, rode todos os casos:

```bash
claude plugin eval plugins/ai-skills --scaffold --allow-tools Write Edit Bash --no-publish
claude plugin eval plugins/ai-skills --case cancel-orders-spec --scaffold --allow-tools Write Edit Bash --no-publish
```

Coloque o caminho do plugin antes das opções que recebem listas. Cada caso roda três vezes em cada braço, com e sem o plugin; `--runs 1` serve para uma conferência rápida. Para avaliar um modelo escolhido por você, passe `--model <modelo>`; os graders `llm` usam o modelo de `--judge-model`. Repita nos modelos que você usa, sem tratar um deles como piso. Cada execução consome o uso normal da sua conta.

Os graders `regex`, `tool_used` e os de rubrica (`llm`) cobrem artefatos, resposta e trace. Com o braço sem plugin, os graders `tool_used` da skill indicam a ativação sem entrar no score; `skill-not-fired` usa `arm: both` e conta nos dois braços. O `claude plugin eval` não tem grader de exit code: `tests-passed` e `suite-passed` julgam pelo trace se a suíte executou testes e terminou com sucesso.

Por padrão, os resultados ficam em `plugins/ai-skills/evals/results/`, fora do Git. Para gravá-los fora da pasta do plugin, passe `--output-dir <pasta>` e `--report <arquivo.html>`. A saída `0` indica todos os casos no limiar, `1` indica caso abaixo do limiar ou erro de carga, e `2` indica execução parcial, por limite de custo ou falha de autenticação. Revise os motivos dos graders antes de interpretar mudanças de score.

## Estrutura

```text
.claude-plugin/marketplace.json    catálogo deste repositório
CLAUDE.md                          orientações para editar o repositório
plugins/ai-skills/
  .claude-plugin/plugin.json       manifesto do plugin
  skills/sdd/
    SKILL.md                       descoberta e encaminhamento
    references/                    procedimentos por etapa
    assets/                        modelos dos artefatos
    scripts/check_spec.py          conferência dos artefatos SDD
  evals/                           casos de claude plugin eval, scaffolds e seed.sh
scripts/validate_repo.py           validação do pacote e da instalação
tests/                             testes dos scripts e das fixtures
```

O formato segue a documentação oficial do Claude Code sobre [plugins](https://code.claude.com/docs/en/plugins), [manifesto](https://code.claude.com/docs/en/plugins/manifest-reference), [marketplaces](https://code.claude.com/docs/en/plugins/marketplace-reference), [skills](https://code.claude.com/docs/en/skills), [evals de plugins](https://code.claude.com/docs/en/plugin-evals) e [CLAUDE.md](https://code.claude.com/docs/en/memory), consultada em 2026-10-09.
