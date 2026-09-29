# ai-skills

Skills do Claude Code para desenvolvimento orientado por especificações, distribuídas como plugin.

| Skill | Finalidade |
|---|---|
| `sdd` | Especificar, planejar, implementar e verificar mudanças, com requisitos EARS rastreáveis da spec ao teste e ADRs. A spec absorve as regras de negócio; o plano traz as decisões técnicas e os checks, cada um com a prova que o decide, sem decompor o trabalho em tarefas. Inclui um verificador de IDs, links e estrutura das specs e dos planos. |

## Instalação

Numa sessão do Claude Code aberta na raiz deste checkout:

```text
/plugin marketplace add ./
/plugin install ai-skills@ai-skills
```

Os mesmos passos pela CLI, fora da sessão:

```bash
claude plugin marketplace add ./
claude plugin install ai-skills@ai-skills
```

O caminho local precisa começar por `./` ou ser absoluto. Se a instalação pedir, rode `/reload-plugins` ou abra uma nova sessão para carregar o plugin. Invoque `/ai-skills:sdd`; o Claude Code também pode selecioná-la quando o pedido corresponde à descrição. Não é necessário configurar MCP, chaves de API ou um modelo fixo.

Para instalar a versão publicada pelo Git, registre o repositório em vez do checkout local:

```bash
claude plugin marketplace add guilhermesalvi/ai-skills
claude plugin install ai-skills@ai-skills
```

O repositório Git, o plugin e o marketplace se chamam `ai-skills`. O catálogo usa caminhos relativos à raiz do repositório. Escolha uma origem por instalação; se já houver um marketplace `ai-skills` registrado de outra origem, remova seu registro com `claude plugin marketplace remove ai-skills` antes de registrar a nova.

Para usar só uma skill, copie `plugins/ai-skills/skills/<nome>` para `~/.claude/skills/<nome>` (todos os projetos) ou `.claude/skills/<nome>` de um projeto. Ela pode ser invocada como `/<nome>`, por exemplo `/sdd`. Escolha entre o plugin e as cópias para não carregar a mesma skill duas vezes.

## Atualização

O manifesto declara uma versão semântica. Ao publicar uma alteração no pacote, incremente `version` em `plugins/ai-skills/.claude-plugin/plugin.json`: sem esse incremento, instalações existentes continuam na versão em cache. Um push não atualiza cópias instaladas por si só. Para uma origem Git:

```bash
claude plugin marketplace update ai-skills
claude plugin update ai-skills@ai-skills
```

Para uma origem local, incremente a versão e repita apenas `claude plugin install ai-skills@ai-skills`. Rode `/reload-plugins` ou abra uma nova sessão após reinstalar; sessões existentes podem continuar com as instruções anteriores. Cópias individuais precisam ser copiadas novamente.

## Convenções

- O pedido do usuário prevalece sobre os defaults das skills. As instruções aplicáveis do repositório consumidor, em `CLAUDE.md` ou `CLAUDE.local.md`, vêm em seguida.
- As instruções das skills estão em português. A prosa dos artefatos gerados segue o pedido, a convenção do repositório e o material de origem, nessa ordem; títulos de seção, rótulos, colunas e campos formam um schema em inglês em qualquer idioma de prosa, e termos canônicos em inglês não se traduzem.
- As skills continuam o trabalho autorizado até a validação e perguntam apenas sobre decisões ausentes que afetem escopo ou correção. Commit e push seguem a autorização do usuário.
- Os scripts exigem Python 3.10+ e não usam pacotes de terceiros. Nos comandos das skills, substitua `<skill-dir>` pela pasta absoluta do `SKILL.md` carregado; execute a partir do projeto consumidor.

## Desenvolvimento

```bash
python -m unittest discover -s tests -v
git diff --check
claude plugin validate . --strict
claude plugin validate plugins/ai-skills --strict
claude plugin validate plugins/ai-skills/skills --strict
```

No Windows, `py -3` pode substituir `python`. As três validações cobrem, na ordem, o catálogo do marketplace, o manifesto do plugin e o frontmatter das skills. Para exercitar uma alteração sem instalar nada, abra a sessão com `claude --plugin-dir ./plugins/ai-skills` e recarregue com `/reload-plugins` a cada edição.

Para testar a instalação sem alterar a configuração pessoal, use um diretório temporário como `CLAUDE_CONFIG_DIR` somente no processo de teste. Em PowerShell, na raiz do repositório:

```powershell
$validationHome = Join-Path ([System.IO.Path]::GetTempPath()) ('ai-skills-' + [guid]::NewGuid())
New-Item -ItemType Directory -Path $validationHome | Out-Null
$previousConfigDir = $env:CLAUDE_CONFIG_DIR
try {
    $env:CLAUDE_CONFIG_DIR = $validationHome
    claude plugin marketplace add ./
    if ($LASTEXITCODE -ne 0) { throw 'Marketplace registration failed' }
    claude plugin install ai-skills@ai-skills
    if ($LASTEXITCODE -ne 0) { throw 'Plugin installation failed' }
    claude plugin details ai-skills
    if ($LASTEXITCODE -ne 0) { throw 'Plugin inspection failed' }
} finally {
    $env:CLAUDE_CONFIG_DIR = $previousConfigDir
}
```

O inventário deve mostrar `ai-skills` habilitado com a skill `sdd`. Esse teste verifica empacotamento e instalação; a qualidade das skills exige uso e revisão dos artefatos. Para testar o seletor na sessão, instale pelo procedimento normal e abra uma nova sessão.

```text
.claude-plugin/marketplace.json      catálogo deste repositório
CLAUDE.md                            orientações para editar o repositório
plugins/ai-skills/
  .claude-plugin/plugin.json         manifesto do plugin
  skills/
    sdd/                             SKILL.md, references/, scripts/check_spec.py
tests/                               testes dos scripts
```

O formato segue a documentação oficial de [plugins](https://code.claude.com/docs/en/plugins), [marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [skills](https://code.claude.com/docs/en/skills) e [CLAUDE.md](https://code.claude.com/docs/en/memory).
