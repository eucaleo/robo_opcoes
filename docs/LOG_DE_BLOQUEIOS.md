# LOG_DE_BLOQUEIOS

## Registro inicial

### Bloqueio semântico e operacional: uso de `data/`

**Descrição:**  
Historicamente, o projeto utilizava `data/` como diretório de armazenamento, o que passou a gerar confusão recorrente com o uso de “data” em contexto temporal.

**Causa provável:**  
Sobrecarga semântica do termo `data`, que em português pode significar tanto:
- dados/armazenamento, por influência de naming técnico;
- data temporal, como dia, mês, ano ou timestamp.

**Impacto observado:**  
- ruído em buscas no repositório;
- dificuldade de interpretação em documentação;
- ambiguidade em tarefas de manutenção;
- maior chance de alteração indevida em trechos temporais;
- perda de precisão em instruções operacionais.

**Decisão de contorno consolidada:**  
Adotar `dados/` como diretório oficial do projeto e tratar `data/` como nomenclatura legada.

**Status do bloqueio:**  
Contornado por decisão documental consolidada.  
Permanece apenas o trabalho operacional de migração incremental do legado.

**Próxima implicação prática:**  
Mapear referências restantes de `data/` para saneamento progressivo.
