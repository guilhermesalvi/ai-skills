# ai-skills

Skills para uso pessoal no Codex, empacotadas como plugin.

O pacote está em beta, na versão `0.1.0-beta.6`, definida em [plugin.json](plugins/ai-skills/plugin.json). Os contratos podem mudar durante o beta, sem compromisso de retrocompatibilidade.

| Skill | Finalidade |
| --- | --- |
| `sdd` | Especificar, preparar, implementar e verificar mudanças com requisitos rastreáveis; registrar decisões em ADRs |

A spec define uma feature, do gatilho ao resultado para o consumidor, com suas regras e alternativas. Em monorepos, as pastas de capabilities agrupam as features; nos demais projetos, as features ficam diretamente em `docs/specs/`. O plano registra decisões técnicas, checks com prova e, quando necessário, itens executáveis com contexto e dependências. Modelos e um validador mantêm IDs, links, schema e rastreabilidade coerentes.

Consulte o [guia de uso da sdd](plugins/ai-skills/skills/sdd/README.md) para exemplos de pedidos, entradas e entregas de cada modo.

## Instalação

Na raiz deste checkout:

```bash
codex plugin marketplace add ./ --json
codex plugin add ai-skills@ai-skills --json
codex plugin list --marketplace ai-skills --json
```

Abra uma nova sessão e invoque `$sdd`. O Codex também seleciona a skill quando o pedido corresponde à descrição dela. O pacote não precisa de MCP nem fixa um modelo. Os scripts da skill exigem Python 3.10+ e Git.

Para instalar a versão publicada no Git:

```bash
codex plugin marketplace add guilhermesalvi/ai-skills --json
codex plugin add ai-skills@ai-skills --json
```

Use uma origem por marketplace. Para trocar entre checkout local e Git, remova o registro anterior com `codex plugin marketplace remove ai-skills` antes de adicionar a nova origem. A origem Git instala a versão publicada; mudanças locais chegam a ela após publicação.

### Skill avulsa

Copie a pasta inteira `plugins/ai-skills/skills/sdd` para `.agents/skills/sdd` de um projeto consumidor ou `~/.agents/skills/sdd` para uso pessoal. Invoque com `$sdd`. Escolha o plugin ou a cópia avulsa para não carregar a mesma skill duas vezes.

Os recursos seguem o padrão aberto [Agent Skills](https://agentskills.io/specification). Resolva os recursos pela pasta absoluta do `SKILL.md` carregado. Nas referências, `<skill-dir>` representa essa pasta; substitua o marcador antes de executar o comando.

## Atualização

Incremente o sufixo beta ao disponibilizar uma nova revisão para seus projetos. Mantenha a versão em `plugins/ai-skills/plugin.json`: a instalação usa essa versão para identificar a cópia em cache.

Para atualizar a origem Git e instalar a revisão atual:

```bash
codex plugin marketplace upgrade ai-skills --json
codex plugin add ai-skills@ai-skills --json
```

Na origem local, registre o checkout novamente com `codex plugin marketplace add ./ --json` e execute `codex plugin add ai-skills@ai-skills --json`. Reinicie o aplicativo e abra uma nova sessão depois de atualizar. Cópias avulsas precisam ser copiadas novamente.

## Convenções

- O pedido prevalece sobre os defaults das skills. Aplique `AGENTS.md` e `AGENTS.override.md` pertinentes do consumidor, respeitando o escopo de diretório.
- Instruções e textos de interface ficam em português. A prosa dos artefatos segue o pedido ou a convenção do consumidor; sem definição, segue o idioma do pedido. O schema permanece em inglês.
- As skills continuam o trabalho autorizado até a validação e perguntam sobre decisões ausentes que afetem escopo ou correção. Commit e push exigem autorização do usuário.
- A verificação SDD usa revisor separado sempre que houver subagente disponível, salvo proibição no pedido ou nas instruções; sem ele, informa que autor e revisor são o mesmo. O pacote não escolhe modelos para o usuário.
- Os scripts usam somente a biblioteca padrão. Execute os comandos da skill a partir do projeto consumidor.

## Desenvolvimento

### Escrita e organização

As instruções são imperativas, com entradas e resultados explícitos, e os recursos são lidos de forma progressiva. O entrypoint apresenta propósito e encaminhamento; cada referência detalha uma etapa quando ela for necessária.

| Conteúdo | Organização |
| --- | --- |
| Contexto, decisão e justificativa | Uma ideia por parágrafo, com evidência pertinente |
| Obrigações e itens paralelos | Bullets com ação e condição claras |
| Comparações e registros com os mesmos campos | Tabelas com cabeçalhos explícitos |
| Dependência real de ordem | Passos numerados |
| Detalhe de uma etapa | Referência indicada no ponto de uso |

EARS, os schemas em inglês, a numeração e os checks rastreáveis são contratos desta skill, não exigências do formato de skills. Mantenha uma fonte por regra e revise instruções conflitantes antes de acrescentar orientações.

Os modelos de spec e plano começam pelas partes centrais e pelas pendências. Os blocos opcionais ficam em `assets/spec-sections.md` e `assets/plan-sections.md`; inclua apenas os que acrescentarem informação ao contrato ou à solução.

Assumptions reúne apenas fatos ainda não verificados e escolhas provisórias, numa lista com um parágrafo por premissa: título curto em negrito, usado nas citações, seguido da afirmação, do fundamento e do impacto de estar errada. Ao resolver uma premissa, mova o resultado para o corpo com evidência ou origem da decisão e atualize as referências afetadas. O fluxo completo está em [premissas e lacunas](plugins/ai-skills/skills/sdd/references/workflow.md#premissas-e-lacunas).

### Checks locais

```bash
python scripts/validate_repo.py
python -B -m unittest discover -s tests -v
python scripts/run_evals.py --fixtures-only
git diff --check
```

No Windows, `py -3` pode substituir `python`. O validador confere o catálogo, o manifesto, a versão semântica, o frontmatter e os links dos recursos da skill. Os testes também semeiam cada fixture das evals e executam seus testes; `resume-contract-conflict` inclui uma regressão local deliberada, que o teste espera ver falhar.

Para verificar a instalação sem modificar sua configuração pessoal:

```bash
python scripts/validate_repo.py --install
```

Esse comando usa um `CODEX_HOME` temporário apenas nos processos filhos e trabalha fora das configurações do projeto. Registra o checkout, instala o plugin, confere versão e habilitação no inventário e compara os arquivos instalados com o pacote. Não precisa de login e apaga o diretório temporário ao terminar. Foi verificado com Codex CLI `0.149.1`.

### Evals

Cada caso em `plugins/ai-skills/evals/` contém `case.json`, `prompt.md`, critérios em `graders/` e, quando necessário, um `scaffold.py`. O runner executa os mesmos scaffolds portáveis dos testes, sem depender de um shell específico.

| Caso | O que confere |
| --- | --- |
| `cancel-orders-spec` | Cancelamento completo, autorização e concorrência, pedido pago como lacuna, premissas, escopo, concisão e entrega |
| `monorepo-feature-specs` | Features independentes em pastas próprias sob a capability, contratos completos, concisão e fontes preservadas |
| `prepare-dependent-change` | Plano transferível, contexto confirmado, dependências reais, provas da integração, pendência limitada à parte afetada e código intacto |
| `adr-from-code` | ADR derivado do código e histórico, sem inventar participantes, alternativas ou motivos |
| `implement-and-verify` | Implementação, testes nomeados nas provas, execução bem-sucedida, checks marcados e relatório |
| `resume-contract-conflict` | Retomada com diff divergente, preservação da spec e nova execução dos checks afetados |
| `ignores-code-review` | Resposta sobre divisão por zero sem carregar a SDD |

Liste os casos ou confira somente as fixtures, sem uso de modelo:

```bash
python scripts/run_evals.py --list
python scripts/run_evals.py --fixtures-only
```

Para avaliar a skill e julgar suas rubricas:

```bash
python scripts/run_evals.py --judge
python scripts/run_evals.py --case cancel-orders-spec --judge
python scripts/run_evals.py --tag spec --tag plan --judge --compare
```

Cada caso roda em um repositório temporário e instala apenas os recursos de execução do plugin: prompts, rubricas e resultados ficam fora do contexto do executor. A configuração também desabilita skills pessoais externas e criação de agentes dentro do harness. O julgamento usa uma execução separada, com permissão de leitura e o plugin desabilitado. O runner copia a autenticação existente para o diretório temporário e a remove ao terminar; execuções reais consomem o uso normal da conta.

Use `--model <modelo>` e `--reasoning-effort <esforço>` para avaliar uma escolha explícita; sem essas opções, vale o padrão da CLI. `--compare` registra também o braço sem plugin. Nesse braço, os critérios positivos de ativação não entram no resultado; a exclusão de code review é julgada nos dois braços.

Os critérios determinísticos conferem arquivos, conteúdo, comandos concluídos com exit code e leitura bem-sucedida do `SKILL.md` como sinal de ativação. A preservação de código compara nomes e hashes antes e depois, incluindo arquivos criados e removidos. As rubricas julgam os artefatos, a resposta final e o trace; a ausência de artefato nunca aprova um critério negativo. Sem `--judge`, as rubricas ficam pendentes.

Os resultados ficam em `eval-results/<timestamp>/`, fora da pasta do plugin e do Git. Use `--output-dir <pasta>` para escolher outro destino. O runner salva resposta, eventos JSONL, stderr, cópia dos arquivos gerados e `report.json`; mantém essa evidência mesmo se o juiz falhar. A saída `0` indica aprovação, `1` indica critérios reprovados e `2` indica erro ou rubrica pendente. Fixtures verdes comprovam o scaffold; a qualidade da skill exige as execuções reais e a leitura dos motivos do julgamento.

## Estrutura

```text
.agents/plugins/marketplace.json  catálogo deste repositório
.codex/config.toml               habilitação do plugin neste projeto
AGENTS.md                        orientações para editar o repositório
plugins/ai-skills/
  plugin.json                    manifesto portável e interface
  skills/sdd/
    SKILL.md                     descoberta e encaminhamento
    agents/openai.yaml           apresentação da skill
    references/                  procedimentos por etapa
    assets/                      modelos dos artefatos
    scripts/check_spec.py        conferência dos artefatos SDD
    scripts/isolated_tree.py     árvores temporárias da verificação
  evals/                         casos, prompts, rubricas e scaffolds
scripts/validate_repo.py         validação do pacote e da instalação
scripts/run_evals.py             execução e julgamento dos cenários
tests/                          testes dos scripts e das fixtures
```

O empacotamento segue a documentação oficial de [plugins](https://developers.openai.com/plugins/build/plugins) e [skills](https://developers.openai.com/codex/skills/), consultada em 2026-10-10. Os comandos de instalação e execução foram conferidos na CLI local.
