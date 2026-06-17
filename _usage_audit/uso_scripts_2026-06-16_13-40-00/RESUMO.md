# Auditoria de uso de scripts antigos

**Data:** Tue Jun 16 13:40:00     2026

**Diretório:** `/c/users/eucal/projeto`

**Modo:** `dry-run`

## Arquivos analisados

- `limpar_repositorio_seguro.sh`
- `find_structure.sh`
- `mapear_repositorio.sh`


## `limpar_repositorio_seguro.sh`

### Arquivos encontrados

- `./limpar_repositorio_seguro.sh`

### Resultado

- Arquivos encontrados: **1**
- Referências no repositório: **4**
- Referências em testes/scripts: **4**
- Relatório de referências: `_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_referencias.txt`
- Histórico Git: `_usage_audit/uso_scripts_2026-06-16_13-40-00/limpar_repositorio_seguro.sh_git_log.txt`

### Decisão

**Não remover automaticamente.** Foram encontradas referências ao arquivo.

Primeiras referências:

```text
./docs/mapeamento_automacao_opcoes_rtd.json:2071:      "path": "limpar_repositorio_seguro.sh",
./docs/mapeamento_automacao_opcoes_rtd.md:1084:### `limpar_repositorio_seguro.sh`
./docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:553:limpar_repositorio_seguro.sh
./docs/validacoes/fase-17-mapa-pastas-arquivos.md:134:limpar_repositorio_seguro.sh
```


## `find_structure.sh`

### Arquivos encontrados

- `./find_structure.sh`

### Resultado

- Arquivos encontrados: **1**
- Referências no repositório: **3**
- Referências em testes/scripts: **3**
- Relatório de referências: `_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_referencias.txt`
- Histórico Git: `_usage_audit/uso_scripts_2026-06-16_13-40-00/find_structure.sh_git_log.txt`

### Decisão

**Não remover automaticamente.** Foram encontradas referências ao arquivo.

Primeiras referências:

```text
./docs/mapeamento_automacao_opcoes_rtd.json:2364:      "path": "find_structure.sh",
./docs/mapeamento_automacao_opcoes_rtd.md:1240:- `find_structure.sh` — `outros` — score `11`
./docs/validacoes/fase-17-mapa-pastas-arquivos.md:133:find_structure.sh
```


## `mapear_repositorio.sh`

### Arquivos encontrados

- `./mapear_repositorio.sh`

### Resultado

- Arquivos encontrados: **1**
- Referências no repositório: **4**
- Referências em testes/scripts: **4**
- Relatório de referências: `_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_referencias.txt`
- Histórico Git: `_usage_audit/uso_scripts_2026-06-16_13-40-00/mapear_repositorio.sh_git_log.txt`

### Decisão

**Não remover automaticamente.** Foram encontradas referências ao arquivo.

Primeiras referências:

```text
./docs/mapeamento_automacao_opcoes_rtd.json:740:      "path": "mapear_repositorio.sh",
./docs/mapeamento_automacao_opcoes_rtd.md:364:### `mapear_repositorio.sh`
./docs/ROTA_MESTRE_2_AUTOMACAO_OPCOES_RTD.md:554:mapear_repositorio.sh
./docs/validacoes/fase-17-mapa-pastas-arquivos.md:137:mapear_repositorio.sh
```

## Status Git final

```text
?? _usage_audit/
?? verificar_uso_scripts_obsoletos.sh
```

