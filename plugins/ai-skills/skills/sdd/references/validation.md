# Validação dos artefatos

Use estas verificações ao revisar um artefato, com profundidade proporcional à mudança.

## Verificações comuns

- Caminhos, links e IDs resolvem para as fontes corretas; numeração não colide e IDs retirados não são reutilizados.
- Idioma, rótulos e formato existentes foram preservados; seções têm conteúdo útil.
- Fatos, hipóteses e decisões ausentes estão distintos; placeholders não fingem que uma decisão foi tomada.
- Exemplos e resultados não foram apresentados como evidência executada.
- Diagramas têm estrutura coerente; o relatório diferencia inspeção textual de renderização.

## Spec

Confira condição e resultado de cada requisito, estabilidade dos IDs, rastreabilidade para o PRD e cobertura dos cenários em escopo. Requisitos precisam permitir uma asserção observável, com limites reais quando aplicáveis. Preserve hipóteses herdadas e impeça decisões de negócio silenciosas.

Confira que cada superfície e cada dimensão têm aterrissagem registrada, e que `n/a` traz o motivo. Um requisito que quantifica sobre um conjunto nomeia os membros ou a fonte que os enumera; uma garantia negativa aponta o mecanismo que a sustenta; um alvo estatístico não ocupa o lugar de um critério. Cada hipótese traz `Confirmed?`, e `y` só vale para o que o usuário decidiu.

Se houver EARS, confira sua consistência. Um formato claro já existente não precisa ser convertido por uniformidade estética.

## Design

Confira critérios e sua origem, alternativas reais, custo da escolha, contratos, responsabilidades e tratamento de falhas. Cada risco material tem mitigação ou aceitação fundamentada. ADRs foram respeitados ou sua substituição está explícita.

Cada requisito em escopo aterrissa em componente, contrato, fluxo ou estrutura de dados. Decisões marcadas como irreversíveis trazem a forma literal e a alternativa rejeitada pela propriedade que a desqualifica. Colocação de arquivo e dependências por componente não fazem parte do documento.

A profundidade acompanha o risco. Um limite de linhas não mede qualidade. Não introduza um mecanismo apenas porque ele aparece em um exemplo desta skill.

## Tarefas

Confira os campos que tornam a tarefa executável: resultado, caminhos já determinados, dependências, requisitos, interfaces, critérios e checks. Dependências existem, são acíclicas e respeitam a ordem de execução. A rastreabilidade funciona nos dois sentidos.

Cada tarefa precisa de evidência adequada ao tipo de alteração. Requisitos com resultado concreto usam esse resultado no critério de conclusão. Comandos vêm da configuração real e não de um template. Não exija a suíte inteira em toda etapa por regra de formatação.

## ADR

Confira alcance da decisão, participantes conhecidos, alternativas avaliadas, critérios comuns e custos concretos. Regras derivadas têm destino real. Referências de substituição são recíprocas. Uma decisão local não vira política de todo o projeto sem necessidade.

## Execução e verificação

Confira se o escopo pedido foi concluído, se evidências correspondem à versão examinada e se limitações estão declaradas. Não marque critérios pendentes como satisfeitos. Corrija inconsistências na fonte e atualize seus dependentes.

Cada evidência nomeia o teste que decide o requisito, traz `arquivo:linha` e observa o resultado no nível que o requisito exige. Conjuntos enumerados têm cobertura por membro. O relatório declara a independência da verificação e se houve injeção de falha.

Ao terminar, relate defeitos concretos e evidências. Repita verificações quando uma mudança, falha ou incerteza real exigir; aproveite resultados que continuam válidos.
