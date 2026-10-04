# ai-skills

Skills para uso pessoal no Codex, empacotadas como plugin no formato portátil Agent Plugins.

O pacote está em beta, na versão `0.1.0-beta.1`, definida em [plugin.json](plugins/ai-skills/plugin.json). A skill `sdd` acompanha a versão do pacote. Os contratos podem mudar durante o beta, sem compromisso de retrocompatibilidade.

| Skill | Finalidade |
| --- | --- |
| `sdd` | Especificar, planejar, implementar e verificar mudanças com requisitos rastreáveis; registrar decisões em ADRs |

A spec define o comportamento e as regras de negócio. O plano registra decisões técnicas e checks com prova. Modelos e um validador mantêm IDs, links, schema e rastreabilidade coerentes.

## Instalação

Com uma CLI do Codex que oferece `codex plugin add`, na raiz deste checkout:

```bash
codex plugin marketplace add ./
codex plugin add ai-skills@ai-skills
codex plugin list --marketplace ai-skills --json
```

No aplicativo, `.agents/plugins/marketplace.json` expõe o catálogo do projeto. Abra o diretório de plugins, selecione o marketplace **AI Skills** e instale **AI Skills**. Reinicie o aplicativo se o catálogo ainda não aparecer. Em projetos confiáveis, `.codex/config.toml` habilita `ai-skills@ai-skills`.

Em uma nova sessão, invoque `$sdd` ou selecione a skill com `/skills`. A descrição também permite seleção automática. O pacote não precisa de MCP nem fixa um modelo. `check_spec.py` exige Python 3.10+ e Git.

Para instalar a versão publicada no Git:

```bash
codex plugin marketplace add guilhermesalvi/ai-skills
codex plugin add ai-skills@ai-skills
```

Use uma origem por marketplace. Para trocar entre checkout local e Git, remova o registro anterior com `codex plugin marketplace remove ai-skills` antes de adicionar a nova origem. A origem Git instala a versão publicada; mudanças locais chegam a ela após publicação.

### Skill avulsa

Copie a pasta inteira `plugins/ai-skills/skills/sdd` para `.agents/skills/sdd` de um projeto consumidor ou `~/.agents/skills/sdd` para uso pessoal. Invoque com `$sdd`. Escolha o plugin ou a cópia avulsa para evitar duas skills com o mesmo nome no seletor.

Os recursos seguem o padrão aberto [Agent Skills](https://agentskills.io/specification). `agents/openai.yaml` acrescenta os metadados de interface do Codex, sem criar dependências de ferramentas.

## Atualização

Incremente o sufixo beta, como de `0.1.0-beta.1` para `0.1.0-beta.2`, ao disponibilizar uma nova revisão para seus projetos. Mantenha a versão em `plugins/ai-skills/plugin.json`. Para atualizar o snapshot de uma origem Git:

```bash
codex plugin marketplace upgrade ai-skills
```

Para recarregar o pacote da origem configurada, reinstale pelo aplicativo ou pela CLI:

```bash
codex plugin remove ai-skills@ai-skills
codex plugin add ai-skills@ai-skills
```

Instalações locais usam uma cópia em cache: editar o checkout não altera essa cópia. Reinstale e abra uma nova sessão. Cópias avulsas precisam ser copiadas novamente. Para desenvolver sem alterar sua instalação pessoal, use a validação isolada abaixo.

## Convenções

- O pedido prevalece sobre os defaults das skills. Aplique `AGENTS.md` e `AGENTS.override.md` pertinentes do consumidor, respeitando o escopo de diretório do Codex.
- Instruções e textos de interface ficam em português. A prosa dos artefatos segue o pedido ou a convenção do consumidor; sem definição, segue o idioma do pedido. O schema permanece em inglês.
- As skills continuam o trabalho autorizado até a validação e perguntam sobre decisões ausentes que afetem escopo ou correção. Commit e push exigem autorização do usuário.
- A verificação SDD usa revisor separado quando disponível e autorizado; sem ele, informa que autor e revisor são o mesmo. O pacote não escolhe modelos para o usuário.
- Os scripts usam somente a biblioteca padrão. Substitua `<skill-dir>` pela pasta absoluta do `SKILL.md` carregado e execute a partir do projeto consumidor.

## Desenvolvimento

### Escrita e organização

As orientações oficiais recomendam instruções imperativas, entradas e resultados explícitos e leitura progressiva dos recursos. O entrypoint apresenta propósito e encaminhamento; cada referência detalha uma etapa quando ela for necessária. Consulte [criação de skills](https://learn.chatgpt.com/docs/build-skills) e [revisão de skills e prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).

| Conteúdo | Organização |
| --- | --- |
| Contexto, decisão e justificativa | Uma ideia por parágrafo, com evidência pertinente |
| Obrigações e itens paralelos | Bullets com ação e condição claras |
| Comparações e registros com os mesmos campos | Tabelas com cabeçalhos explícitos |
| Dependência real de ordem | Passos numerados |
| Detalhe de uma etapa | Referência indicada no ponto de uso |

EARS, os schemas em inglês, a numeração e os checks rastreáveis são contratos desta skill. Eles não são exigências da OpenAI para toda skill. Mantenha uma fonte por regra e revise instruções conflitantes antes de acrescentar mais orientações.

Os modelos de spec e plano começam pelas partes centrais e pelas pendências. Os blocos opcionais ficam em `assets/spec-sections.md` e `assets/plan-sections.md`; inclua apenas os que acrescentarem informação ao contrato ou à solução.

Assumptions reúne apenas fatos ainda não verificados e escolhas provisórias, em parágrafos com a afirmação em negrito, seu fundamento e o impacto de estar errada. Ao resolver uma premissa, mova o resultado para o corpo com evidência ou origem da decisão e atualize as referências afetadas. O fluxo completo está em [premissas e lacunas](plugins/ai-skills/skills/sdd/references/workflow.md#premissas-e-lacunas).

### Checks locais

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

No Windows, `py -3` pode substituir `python`. O validador confere o catálogo, os campos usados pelo manifesto portátil, o frontmatter e os links dos recursos. É específico deste repositório e não substitui a revisão de publicação da OpenAI.

Para verificar a instalação sem modificar sua configuração pessoal:

```bash
python scripts/validate_repo.py --install
```

Esse comando cria um `CODEX_HOME` temporário apenas nos processos filhos, registra o checkout, instala o plugin, inspeciona o inventário e compara os recursos instalados com o pacote. Não precisa de login e apaga o diretório temporário ao terminar. Foi verificado com Codex CLI `0.149.1`.

### Evals

Os casos em `plugins/ai-skills/evals/` usam um runner próprio com `codex exec --json`, conforme a [orientação oficial para avaliar skills](https://developers.openai.com/blog/eval-skills).

| Caso | O que confere |
| --- | --- |
| `cancel-orders-spec` | Capability, idioma, dimensões, autorização, pedido pago como lacuna, premissas abertas e origem das decisões, escopo do plano, concisão e entrega |
| `adr-from-code` | ADR derivado do código e histórico, sem inventar participantes, alternativas ou motivos |
| `implement-and-verify` | Implementação, testes nomeados nas provas, execução bem-sucedida, checks marcados e relatório |
| `resume-contract-conflict` | Retomada com diff divergente, preservação da spec e nova execução dos checks afetados |
| `ignores-code-review` | Resposta sobre divisão por zero sem carregar a SDD |

Liste os casos ou confira os scaffolds sem chamar um modelo:

```bash
python scripts/run_evals.py --list
python scripts/run_evals.py --fixtures-only
```

Fixtures normalmente têm testes verdes na origem. `resume-contract-conflict` inclui uma regressão local deliberada; seu `fixture_test_exit_code` declara a falha esperada na conferência offline. A avaliação com o modelo só passa depois da correção e dos testes verdes.

Execute com a autenticação existente do Codex:

```bash
python scripts/run_evals.py --judge
python scripts/run_evals.py --case cancel-orders-spec --judge
```

O runner cria cada fixture Git fora deste repositório, instala o plugin em uma configuração temporária e captura eventos JSONL, resposta e arquivos gerados. A instalação vem de uma cópia temporária dos recursos de runtime, sem a pasta `evals`, para não expor prompts e rubricas ao executor. Marca como confiável apenas o workspace que acabou de gerar, mantendo o sandbox do caso.

Reutiliza apenas `auth.json`, quando existente, numa cópia temporária removida ao terminar; variáveis de autenticação por API também podem ser usadas. Não copia sua configuração, instruções ou plugins pessoais. Os scaffolds são Python e funcionam no Windows, macOS e Linux.

Os casos selecionam os perfis de permissões `:workspace`, ou `:read-only` para code review; o julgamento das rubricas também usa `:read-only`. Esses perfis exigem uma CLI atual. O runner não pede aprovação interativa nem remove o sandbox. Falhas de autenticação, acesso ao workspace ou timeout são erros de execução.

No Windows, a configuração temporária usa o sandbox nativo `unelevated`, com token restrito, para dispensar setup administrativo na execução isolada. O runner ajusta as ACLs apenas da pasta descartável: permite leitura dos recursos do plugin e edição do fixture, sem propagar essas permissões para `auth.json`. A instalação pessoal mantém sua configuração.

Checks determinísticos examinam artefatos e eventos `command_execution`. Uma leitura de `sdd/SKILL.md` com exit code `0` e o campo `name: sdd` na saída é o sinal observável de ativação, uma aproximação pelo trace. Isso evita contar um pipeline que termina com sucesso após falhar na leitura. Rubricas de conteúdo usam uma segunda execução com `--output-schema` quando `--judge` é passado. Sem essa opção, ficam pendentes e a execução termina com código `2`.

Adicione `--compare` para registrar uma execução independente sem o plugin. O baseline serve para comparação; somente o resultado com plugin decide aprovação. Para avaliar um modelo escolhido por você, passe `--model <modelo>`; sem a opção, vale o default da CLI na configuração temporária. Cada execução consome o uso normal do Codex.

Use `--reasoning-effort <esforço>` para escolher o mesmo esforço na geração e no julgamento. Sem essa opção, vale o default do modelo na CLI isolada, que pode diferir da sua configuração pessoal. O relatório registra modelo e esforço explícitos; níveis disponíveis dependem do modelo e do cliente, conforme a [referência de configuração](https://learn.chatgpt.com/docs/config-file/config-reference).

Para comparar os modelos escolhidos neste projeto, execute os mesmos casos e rubricas em cada um:

```bash
python scripts/run_evals.py --model gpt-5.6-luna --judge
python scripts/run_evals.py --model gpt-6-astra --judge
```

Esses comandos não alteram o modelo do consumidor. Aprovação nos casos exercitados mostra evidência para esses pedidos; não garante desempenho igual em toda tarefa. Compare também os artefatos e os motivos do julgamento, além dos checks determinísticos.

O runner usa a CLI encontrada no `PATH`. Se ela não reconhecer o modelo escolhido, passe `--codex <caminho-do-executável>` para usar outra instalação, sem alterar o `PATH` ou a configuração pessoal.

Resultados ficam em `plugins/ai-skills/evals/results/`, fora do Git. Saídas: `0` para aprovação, `1` para check reprovado e `2` para erro de execução ou rubrica pendente. Revise evidências e motivos das rubricas antes de interpretar mudanças de score.

## Estrutura

```text
.agents/plugins/marketplace.json    catálogo Codex deste repositório
.codex/config.toml                 habilitação no projeto confiável
AGENTS.md                          orientações para editar o repositório
plugins/ai-skills/
  plugin.json                      manifesto portátil e interface OpenAI
  skills/sdd/
    SKILL.md                       descoberta e encaminhamento
    agents/openai.yaml             interface da skill no Codex
    references/                    procedimentos por etapa
    assets/                        modelos dos artefatos
    scripts/check_spec.py          conferência dos artefatos SDD
  evals/                           prompts, case.json, scaffolds e rubricas
scripts/                           validação do pacote e runner Codex
tests/                             testes dos scripts e fixtures
```

O formato segue as orientações oficiais de [skills](https://learn.chatgpt.com/docs/build-skills), [empacotamento e marketplaces](https://developers.openai.com/plugins/build/plugins) e [revisão de instruções](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), consultadas em 2026-10-04. Para configuração e execução, consulte [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) e [modo não interativo](https://learn.chatgpt.com/docs/non-interactive-mode). A OpenAI recomenda `plugin.json` portátil para novos pacotes; `.codex-plugin/plugin.json` permanece uma opção de compatibilidade, sem necessidade de duplicar manifestos neste projeto.
