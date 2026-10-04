# Orientações do repositório

Este repositório distribui a skill `sdd` no plugin `ai-skills` para Codex. O pacote fica em `plugins/ai-skills/`, com manifesto portátil `plugin.json`, e o marketplace em `.agents/plugins/marketplace.json`. `.codex/config.toml` habilita o plugin neste projeto quando ele é confiável.

Instruções, referências e textos de interface ficam em português. Código, identificadores, comentários, mensagens dos scripts e commits ficam em inglês. Títulos de seção, rótulos, colunas e campos dos artefatos gerados formam um schema em inglês, definido nas referências. Termos canônicos, como EARS, NFR e trade-off, não se traduzem.

## Editar as skills

- Preserve o `name` da skill. O `description` orienta a seleção automática: descreva a capacidade, os gatilhos e as exclusões relevantes de forma concisa. A invocação explícita usa `$sdd`; não desabilite a seleção automática sem pedido.
- Mantenha propósito, limites e encaminhamento no `SKILL.md`. Procedimentos condicionais ficam em `references/`, operações determinísticas em `scripts/` e modelos em `assets/`. Metadados de interface do Codex ficam em `agents/openai.yaml`.
- Resolva recursos a partir da pasta do `SKILL.md` carregado. `<skill-dir>` representa esse caminho absoluto, não uma variável do Codex. Execute os comandos a partir do projeto consumidor.
- Inclua apenas orientações que mudem decisões ou preservem contratos. Não repita instruções gerais do agente, regras já presentes em contexto nem conteúdo das referências no entrypoint.
- Cada regra tem uma única fonte; schemas e suas validações determinísticas precisam concordar. A conferência final pode reunir os critérios de julgamento que os scripts não cobrem.
- Escreva instruções imperativas com critérios de resultado. Use sequência fixa só onde a ordem importa e explique restrições não óbvias. Não imponha contagens de rodadas, tamanho de saída ou limiares sem fundamento.
- Organize referências por assunto; referências extensas podem abrir com `Conteúdo:` para facilitar leitura parcial. Diga quando ler uma referência no ponto que encaminha para ela.
- Mantenha cada skill independente, sem links para outras skills. Convenções do consumidor vêm de `AGENTS.md` e `AGENTS.override.md` aplicáveis; o pedido e essas convenções prevalecem sobre defaults da skill.
- Não fixe modelo, provedor ou piso por família de modelos. Avalie nos modelos que o usuário escolhe, sem compensar limitações hipotéticas com instruções extras.
- Preserve alterações locais existentes. Siga o escopo e a autorização do usuário; escolhas rotineiras, edições e validações já autorizadas não exigem nova aprovação.

## Validar

Os scripts usam Python 3.10+ e somente a biblioteca padrão. No Windows, `py -3` pode substituir `python`.

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

Depois de alterar empacotamento, execute `python scripts/validate_repo.py --install` para instalar e inspecionar o plugin em uma configuração temporária. Depois de alterar comportamento da skill, execute os casos pertinentes com `python scripts/run_evals.py`, conforme o README. Confira ativação, artefatos e rubricas qualitativas; uma rubrica pendente não é aprovação. Não crie testes que só repetem o texto das instruções.

## Commits

Mensagens seguem `<type>: <description>`, em inglês, com até 60 caracteres, descrição no imperativo e inicial minúscula. Tipos: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `style`, `revert`. Sem escopo, ponto final, `!`, corpo ou trailers.

Agrupe por motivo: skill, scripts e testes da mesma mudança ficam no mesmo commit; motivos independentes, em commits separados. Faça commit e push só com autorização do usuário.
