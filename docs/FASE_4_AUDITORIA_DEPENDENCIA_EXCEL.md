# Fase 4 - Auditoria de Dependência do Excel

## Objetivo

Descobrir exatamente onde o sistema ainda depende de abas do Excel, CSVs derivados antigos, leituras diretas da pasta bridge, arquivos temporários ou cálculos prontos vindos da planilha.

Esta fase não altera regra de negócio nem código de produção.

## Base de referência

Documento anterior:

```text
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md
```

Branch esperada:

```text
limpeza-tests-scripts-checks
```

## Critério de saída

```text
Lista objetiva de arquivos e funções que ainda dependem do Excel como fonte operacional.
```

## 1. Auditoria bruta

### Branch atual

```text
limpeza-tests-scripts-checks
```

### Status Git

```text
?? docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md
```

### Últimos commits

```text
d73f757 Alinha fase 3 com rota mestre
7ab90a6 Classifica fontes de dados da fase 3
6167c32 Documenta diagnostico do fluxo atual da fase 2
0fc0495 Remove duplicidade de testes de carga do editor de estruturas
800e150 Consolida testes de endpoints de legs de estruturas
```

### Referências a abas críticas do Excel

```text
db/import_excel.py:9:    "CONFIGURACOES": "robo_config",
db/import_excel.py:10:    "ANALISE_ROBO": "robo_snapshot",
db/import_excel.py:11:    "ANALISE_ROBO_LEGS": "robo_legs_snapshot",
db/import_excel.py:12:    "HIST_ROBO": "robo_legs_history",
db/import_excel.py:13:    "ENCERRAMENTOS_MANUAIS": "encerramentos_manuais",
db/schema_excel.py:16:-- Snapshot agregado por ABA (ANALISE_ROBO)
db/schema_excel.py:37:-- Snapshot por perna (ANALISE_ROBO_LEGS)
db/schema_excel.py:67:-- Histórico por perna (HIST_ROBO) (parece similar ao legs, mas sem alguns campos)
```

### Referências a CSVs derivados antigos

```text
ATT/checks/check_end_to_end.py:15:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
ATT/checks/check_end_to_end.py:16:    ROOT_DIR / "bridge" / "analise_robo.csv",
ATT/checks/check_end_to_end.py:17:    ROOT_DIR / "bridge" / "analise_raiox.csv",
ATT/checks/check_legs.py:12:    BRIDGE_DIR / "analise_robo_legs.csv",
ATT/checks/check_legs.py:13:    BRIDGE_DIR / "analise_robo.csv",
ATT/checks/check_legs.py:14:    BRIDGE_DIR / "analise_raiox.csv",
ATT/checks/check_structures.py:15:    ROOT_DIR / "bridge" / "analise_robo.csv",
ATT/checks/check_structures.py:16:    ROOT_DIR / "bridge" / "analise_robo_legs.csv",
UI/models/ui_data.py:16:    "rtd_consolidacoes",
bridge_ingest_csv.py:33:    CsvSpec("analise_raiox.csv",          "rtd_analise_raiox",          "replace"),
bridge_ingest_csv.py:34:    CsvSpec("consolidacoes.csv",           "rtd_consolidacoes",           "replace"),
bridge_ingest_csv.py:35:    CsvSpec("analise_robo.csv",            "rtd_analise_robo",            "replace"),
bridge_ingest_csv.py:36:    CsvSpec("analise_robo_legs.csv",       "rtd_analise_robo_legs",       "replace"),
bridge_ingest_csv.py:39:    CsvSpec("rolls_detectados.csv",        "rtd_rolls_detectados",        "append"),
bridge_ingest_csv.py:40:    CsvSpec("hist_robo.csv",               "rtd_hist_robo",               "append"),
bridge_ingest_csv.py:41:    CsvSpec("encerramentos_manuais.csv",   "rtd_encerramentos_manuais",   "append"),
db/import_excel.py:13:    "ENCERRAMENTOS_MANUAIS": "encerramentos_manuais",
db/schema_excel.py:90:CREATE TABLE IF NOT EXISTS encerramentos_manuais (
db/schema_excel.py:103:CREATE INDEX IF NOT EXISTS ix_encerramentos_data ON encerramentos_manuais(data);
domain/market_snapshot.py:58:    Agrega o cabeçalho da estrutura (rtd_analise_robo) e suas legs.
repositories/market_snapshot_repository.py:5:Le legs RTD (rtd_analise_robo_legs) e manuais (manual_analise_robo_legs),
repositories/market_snapshot_repository.py:50:    FROM rtd_analise_robo_legs
repositories/market_snapshot_repository.py:79:    FROM manual_analise_robo_legs
repositories/market_snapshot_repository.py:98:    FROM rtd_analise_robo
repositories/robo_legs_repository.py:35:      manual_analise_robo_legs > rtd_analise_robo_legs
repositories/robo_legs_repository.py:63:            table="manual_analise_robo_legs",
repositories/robo_legs_repository.py:72:            table="rtd_analise_robo_legs",
repositories/robo_legs_repository.py:87:            FROM manual_analise_robo_legs
repositories/robo_legs_repository.py:109:                    SELECT timestamp FROM manual_analise_robo_legs WHERE aba = ?
repositories/robo_legs_repository.py:111:                    SELECT timestamp FROM rtd_analise_robo_legs WHERE aba = ?
repositories/robo_legs_repository.py:119:                "SELECT DISTINCT timestamp FROM manual_analise_robo_legs "
repositories/robo_legs_repository.py:127:                "SELECT DISTINCT timestamp FROM rtd_analise_robo_legs "
repositories/robo_legs_status_repository.py:53:                "SELECT MAX(timestamp) AS ts FROM manual_analise_robo_legs WHERE aba = ?",
repositories/robo_legs_status_repository.py:57:                "SELECT MAX(timestamp) AS ts FROM rtd_analise_robo_legs WHERE aba = ?",
services/canonical_pricing_facade.py:136:      rtd_analise_robo.aba = SMAL11
services/canonical_pricing_facade.py:137:      rtd_analise_robo.spot = 124.66
```

### Leituras diretas da pasta bridge

```text
ATT/checks/check_end_to_end.py:14:BRIDGE_FILES = [
ATT/checks/check_end_to_end.py:97:        require_any(BRIDGE_FILES, "bridge")
ATT/checks/check_legs.py:9:BRIDGE_DIR = ROOT_DIR / "bridge"
ATT/checks/check_legs.py:12:    BRIDGE_DIR / "analise_robo_legs.csv",
ATT/checks/check_legs.py:13:    BRIDGE_DIR / "analise_robo.csv",
ATT/checks/check_legs.py:14:    BRIDGE_DIR / "analise_raiox.csv",
ATT/checks/check_structures.py:14:BRIDGE_CANDIDATES = [
ATT/checks/check_structures.py:76:        require_any(BRIDGE_CANDIDATES, "bridge/estrutura")
bridge_ingest_csv.py:18:BRIDGE_DIR = PROJECT_DIR / "bridge"
bridge_ingest_csv.py:198:            path = BRIDGE_DIR / spec.filename
bridge_ingest_csv.py:220:    parser = argparse.ArgumentParser(description="Ingest CSVs do bridge/ para dados/app.db")
bridge_ingest_csv.py:233:    BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
bridge_ingest_csv.py:234:    control = BRIDGE_DIR / "last_export.txt"
bridge_ingest_csv.py:243:    print(f"[INGEST] Bridge dir: {BRIDGE_DIR}")
domain/calculation_request.py:207:    O orquestrador monta este objeto a partir do DB e do bridge/RTD,
services/canonical_input_service.py:54:            # BRIDGE LEGADO: import dinamico de robo_legs_service para compatibilidade
```

### Dependências técnicas de Excel

```text
ATT/checks/check_api_routes.py:6:    import win32com.client
ATT/checks/check_api_routes.py:8:    win32com = None
ATT/checks/check_api_routes.py:13:    ROOT_DIR / "LISTA_RTD.xlsm",
ATT/checks/check_api_routes.py:14:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
ATT/checks/check_api_routes.py:27:        "Nenhum workbook principal encontrado: LISTA_RTD.xlsm/xlsx"
ATT/checks/check_api_routes.py:33:        log("INFO", "Iniciando check local do runtime Excel")
ATT/checks/check_api_routes.py:35:        if win32com is None:
ATT/checks/check_api_routes.py:41:        excel = win32com.client.Dispatch("Excel.Application")
ATT/checks/check_api_routes.py:43:        log("OK", "Excel COM iniciado com sucesso")
ATT/checks/check_api_routes.py:45:        wb = excel.Workbooks.Open(str(workbook_path))
ATT/checks/check_api_routes.py:48:        sheet_count = wb.Worksheets.Count
ATT/checks/check_api_routes.py:54:        first_sheet = wb.Worksheets(1)
ATT/checks/check_api_routes.py:61:        log("OK", "Check de Excel local concluído com sucesso")
ATT/checks/check_api_routes.py:65:        log("FAIL", f"Erro no check de Excel local: {e}")
ATT/checks/check_end_to_end.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
ATT/checks/check_end_to_end.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
ATT/checks/check_structures.py:10:    ROOT_DIR / "LISTA_RTD.xlsm",
ATT/checks/check_structures.py:11:    ROOT_DIR / "OPERACOES_E_OPCOES.xlsx",
UI/main_window.py:508:* Excel RTD  CSV Bridge
db/import_excel.py:6:XLSX_PATH = "OPERACOES_E_OPCOES.xlsx"  # ajuste se estiver em outra pasta
db/import_excel.py:71:    # drop colunas lixo do Excel
db/import_excel.py:91:        df = pd.read_excel(XLSX_PATH, sheet_name=sheet)
utils/leg_normalizers.py:50:        Converte serial date do Excel para datetime.
utils/leg_normalizers.py:51:        Base prática compatível com pandas/openpyxl:
utils/leg_normalizers.py:59:        Tenta interpretar value como serial do Excel.
utils/leg_normalizers.py:91:        """Parser robusto para timestamp, incluindo serial Excel."""
utils/leg_normalizers.py:101:        # tenta serial Excel cedo, antes do pandas genérico
```

### Leituras de CSV em código Python

```text
ATT/checks/check_legs.py:34:def read_csv_rows(path: Path):
ATT/checks/check_legs.py:41:        rows = list(csv.reader(StringIO(text), dialect))
ATT/checks/check_legs.py:45:        rows = list(csv.reader(StringIO(text), delimiter=delimiter))
ATT/checks/check_legs.py:51:    rows, delimiter, encoding = read_csv_rows(path)
bridge_ingest_csv.py:89:        df = pd.read_csv(
bridge_ingest_csv.py:106:def read_csv(path: Path) -> pd.DataFrame:
bridge_ingest_csv.py:203:            df = read_csv(path)
```

## 2. Classificação preliminar

### 2.1 Dependência direta de Excel

Arquivos identificados:

```text
db/import_excel.py
db/schema_excel.py
ATT/checks/check_api_routes.py
ATT/checks/check_end_to_end.py
ATT/checks/check_structures.py
```

Classificação:

```text
Dependência direta ou legado de Excel.
```

Detalhe:

- `db/import_excel.py` é o ponto mais crítico de dependência direta.
- Ele lê diretamente `OPERACOES_E_OPCOES.xlsx` usando `pd.read_excel`.
- Ele mapeia abas críticas do Excel para tabelas internas:
  - `CONFIGURACOES`
  - `ANALISE_ROBO`
  - `ANALISE_ROBO_LEGS`
  - `HIST_ROBO`
  - `ENCERRAMENTOS_MANUAIS`
- `db/schema_excel.py` não lê Excel diretamente, mas define estrutura associada ao modelo importado do Excel.
- Os arquivos em `ATT/checks/` fazem validações locais envolvendo workbook Excel, `win32com` ou presença de `LISTA_RTD.xlsm/xlsx`.

Conclusão parcial:

```text
A dependência direta real de Excel em código operacional está concentrada em db/import_excel.py.
Os demais pontos são schema legado ou checks auxiliares.
```

### 2.2 Dependência operacional de CSVs derivados do bridge

Arquivo identificado:

```text
bridge_ingest_csv.py
```

Classificação:

```text
Dependência operacional ativa de CSVs derivados do bridge.
```

CSVs identificados:

```text
analise_raiox.csv
consolidacoes.csv
analise_robo.csv
analise_robo_legs.csv
rolls_detectados.csv
hist_robo.csv
encerramentos_manuais.csv
```

Tabelas alimentadas:

```text
rtd_analise_raiox
rtd_consolidacoes
rtd_analise_robo
rtd_analise_robo_legs
rtd_rolls_detectados
rtd_hist_robo
rtd_encerramentos_manuais
```

Conclusão parcial:

```text
bridge_ingest_csv.py é o principal ponto de acoplamento operacional entre arquivos CSV exportados pelo bridge e o banco dados/app.db.
```

### 2.3 Dependência indireta de tabelas derivadas do Excel/bridge

Arquivos identificados:

```text
repositories/market_snapshot_repository.py
repositories/robo_legs_repository.py
repositories/robo_legs_status_repository.py
domain/market_snapshot.py
services/canonical_pricing_facade.py
UI/models/ui_data.py
```

Classificação:

```text
Dependência indireta.
```

Detalhe:

Esses arquivos não leem Excel nem CSV diretamente, mas consomem tabelas que são alimentadas por dados vindos do bridge/RTD ou de estruturas manuais equivalentes.

Principais tabelas:

```text
rtd_analise_robo
rtd_analise_robo_legs
manual_analise_robo_legs
rtd_consolidacoes
```

Conclusão parcial:

```text
A camada de domínio e repositórios já está majoritariamente desacoplada de arquivo físico, mas ainda depende semanticamente das tabelas rtd_* e manual_*.
```

### 2.4 Itens legados ou compatíveis que não são bloqueadores imediatos

Arquivos identificados:

```text
utils/leg_normalizers.py
UI/main_window.py
ATT/tests/test_robo_legs_repository.py
ATT/tests/test_robo_legs_status_repository.py
```

Classificação:

```text
Compatibilidade, documentação visual ou teste.
```

Detalhe:

- `utils/leg_normalizers.py` converte serial date do Excel, mas não lê Excel.
- `UI/main_window.py` apenas menciona visualmente o fluxo `Excel RTD CSV Bridge`.
- Os testes criam tabelas `manual_*` e `rtd_*` para validar comportamento dos repositórios.

Conclusão parcial:

```text
Esses pontos não devem ser tratados como fonte operacional direta, mas devem ser considerados em futura renomeação ou migração semântica das tabelas.
```

## 3. Conclusão

A auditoria da Fase 4 identificou que a dependência do Excel está concentrada em poucos pontos.

### Lista objetiva de arquivos e funções/pontos que ainda dependem do Excel ou bridge como fonte operacional

#### Dependência direta de Excel

```text
db/import_excel.py
```

Ponto crítico:

```text
pd.read_excel(XLSX_PATH, sheet_name=sheet)
```

Abas críticas:

```text
CONFIGURACOES
ANALISE_ROBO
ANALISE_ROBO_LEGS
HIST_ROBO
ENCERRAMENTOS_MANUAIS
```

#### Dependência operacional de CSV bridge

```text
bridge_ingest_csv.py
```

Pontos críticos:

```text
BRIDGE_DIR = PROJECT_DIR / "bridge"
CsvSpec(...)
pd.read_csv(...)
read_csv(path)
```

CSVs críticos:

```text
analise_raiox.csv
consolidacoes.csv
analise_robo.csv
analise_robo_legs.csv
rolls_detectados.csv
hist_robo.csv
encerramentos_manuais.csv
```

#### Dependência indireta por tabelas RTD/manuais

```text
repositories/market_snapshot_repository.py
repositories/robo_legs_repository.py
repositories/robo_legs_status_repository.py
domain/market_snapshot.py
services/canonical_pricing_facade.py
UI/models/ui_data.py
```

Tabelas críticas:

```text
rtd_analise_robo
rtd_analise_robo_legs
manual_analise_robo_legs
rtd_consolidacoes
```

### Fechamento da fase

```text
A Fase 4 cumpriu o critério de saída.
A dependência direta de Excel está concentrada em db/import_excel.py.
A dependência operacional atual está concentrada em bridge_ingest_csv.py.
A aplicação consome majoritariamente tabelas SQLite, mas essas tabelas ainda carregam semântica e origem de dados do bridge/Excel.
```

### Próxima fase recomendada

```text
Fase 5 - Isolar formalmente o bridge/Excel como adaptador legado e definir quais tabelas passam a ser fonte canônica, quais continuam temporárias e quais devem ser migradas ou renomeadas.
```
