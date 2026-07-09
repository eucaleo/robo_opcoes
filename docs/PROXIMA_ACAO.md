# PROXIMA_ACAO

## Próxima ação prioritária

Executar um levantamento objetivo de todas as ocorrências de `data/` no repositório para classificar o que é:

- referência legada de diretório;
- uso legítimo da palavra “data” em contexto temporal;
- falso positivo sem impacto estrutural.

---

## Objetivo

Separar com precisão o que deve ser migrado para `dados/` do que deve permanecer como referência temporal.

---

## Passos concretos

1. Buscar no repositório por:
   - `data/`
   - `/data`
   - `"data"`
   - `'data'`

2. Classificar os resultados em grupos:
   - **migrar para `dados/`**
   - **manter por contexto temporal**
   - **avaliar manualmente**

3. Registrar o resultado em documento técnico ou diário.

4. Definir a primeira substituição segura de baixo risco.

---

## Critério de sucesso

A ação será considerada concluída quando houver:

- lista inicial de ocorrências mapeadas;
- separação entre diretório legada e termo temporal;
- indicação clara do primeiro ajuste seguro a executar.

---

## Ponto de recuperação

Se a tarefa for interrompida, retomar diretamente pelo levantamento textual de ocorrências de `data` e continuar a classificação sem reavaliar a decisão estrutural, pois ela já está consolidada.

---

## Importante

A decisão de usar `dados/` já está definida. Esta ação não é para rediscutir a convenção, mas apenas para operacionalizar a limpeza incremental do legado.

## Status da conferência de paths legados

Foi executada varredura objetiva para localizar referências operacionais a:

- `data/app.db`
- `data/derived.db`

Após os ajustes aplicados, não restaram referências operacionais ativas no código principal.

As únicas ocorrências residuais ficaram restritas a:
- utilitário de auditoria (`scripts/scan_data_references.py`);
- backups temporários gerados durante o patch;
- artefatos históricos e relatórios, excluídos da conferência operacional.

Conclusão:
a migração operacional de `data/` para `dados/` encontra-se saneada para os bancos principais.
