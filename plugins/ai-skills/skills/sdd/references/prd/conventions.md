# Convenções dos PRDs

## Cabeçalho

O PRD de uma capability começa pelo título, que é o nome da capability, e por uma tabela de cabeçalho:

```markdown
# Emissão de fatura

| | |
| --- | --- |
| **Prefixo dos requisitos** | `INV` |
| **Capabilities afetadas** | Notificação ao cliente, Contabilização |
| **Visão geral** | [Visão geral](../overview.md) |
```

- Inclua Capabilities afetadas quando o PRD muda o que outras capabilities recebem ou observam, e explique o impacto em Dependências e riscos. Cite cada uma pelo título do PRD dela. Sem capability afetada, omita a linha.
- Inclua Visão geral quando ela existir; sem ela, omita a linha.

## IDs

O ID de um requisito começa pelo prefixo do PRD que o define, para que uma citação em outro PRD, numa spec ou num teste indique onde está a definição. O prefixo abrevia a capability, em letras maiúsculas e dígitos, começando por letra, como `INV` para Emissão de fatura ou `DOC` para Verificação de documentos. Não abrevie a área a que a capability pertence: o prefixo se repetiria quando a área ganhasse o segundo PRD. Evite nomes genéricos como `REQ`, que não indicam o dono, e não use `FR` nem `NFR`, que o verificador trata como ID sem prefixo. Num PRD novo, escolha um prefixo que nenhum outro PRD use e, se existir a visão geral, registre a capability e o prefixo na seção Capabilities dela; ao editar, mantenha o prefixo existente.

O ID tem a forma `<PREFIX>-nn`, com uma única sequência por PRD para requisitos funcionais e não funcionais. O tipo é dado pela seção onde o requisito é definido, Requisitos funcionais ou Requisitos não funcionais, e não pelo ID; assim, reclassificar um requisito muda a seção sem mudar o ID. Numere com pelo menos dois dígitos (`01`, `02`) e, depois de `99`, siga para `100`.

Defina cada requisito num item de lista que começa pelo ID em negrito, com a prioridade MoSCoW (Must, Should, Could, Won't) entre parênteses dentro do negrito:

```markdown
## Requisitos funcionais

- **INV-01 (Must)** Quando a fatura for emitida, o sistema informa seu número ao cliente.

## Requisitos não funcionais

- **INV-02 (Should)** O número é informado em até 2 segundos após a emissão, no percentil 95.
```

Todo ID citado precisa estar definido num PRD do projeto e corresponder ao requisito que o texto pretende citar.

Antes de alterar ou retirar um requisito ou um caso de aceitação, procure seus IDs e o nome do caso com `git grep -n` para encontrar os PRDs, specs e testes que dependem deles.

Um requisito novo recebe o número seguinte ao maior já usado com o mesmo prefixo. Um ID retirado some do arquivo, então confira com `git log -S "<ID>"` que o número nunca existiu antes de atribuí-lo. Um ID retirado não volta a ser usado, e os demais não são renumerados para fechar buracos na sequência.

Quando estados, motivos ou outras enumerações tiverem valores referenciados pelo código ou pelos contratos, liste-os numa tabela com a coluna Identificador ao lado do nome de exibição. O Identificador traz o nome estável do valor, como `UnderReview`, e permite mudar o nome de exibição sem mudar a identidade do conceito.
