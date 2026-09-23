# Glossário: exceções e consolidação

## Exceção por ocorrência

Uma exceção contextual a um mapeamento confirmado não entra na consolidação. Registre-a em `work/<run>/overrides/NN.json`, com a expressão original, o horário ou contexto próximo, a ação e a evidência.

A exceção vale só naquela ocorrência: ocorrência não resolvida fica `original [?]`, e o mapeamento confirmado continua valendo nos outros pontos.

## Repetir ou recuperar o merge

O recibo torna o `merge` seguro para repetir: rodar de novo com os mesmos candidatos conclui ou reconhece a consolidação anterior sem duplicá-la. Para recuperar uma consolidação interrompida, a referência é o recibo gravado antes da troca atômica do glossário, não o estado do plano.

Se candidatos ou glossário mudaram de forma incompatível com o recibo, concilie o estado em vez de apagar o recibo. Resoluções posteriores à consolidação usam outro lote de candidatos, com outro recibo.

## Glossário compartilhado entre aulas

Serialize as consolidações de aulas que compartilham o glossário: só um coordenador consolida por vez.
