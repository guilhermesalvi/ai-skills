---
description: Revisão de código sem spec, que a descrição da skill exclui.
tags: [trigger]
max_turns: 10
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: A resposta aponta a divisão por zero sem carregar a skill sdd.
---

Revise esta função e diga se tem bug:

```python
def average(values):
    return sum(values) / len(values)
```
