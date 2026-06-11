# Fase 5 - Isolamento do Bridge/Excel como Adaptador Legado

## Objetivo

Isolar formalmente o Excel e o bridge CSV como adaptadores legados, separando origem física de dados, tabelas intermediárias e modelo canônico usado pela aplicação.

Esta fase não deve alterar regra de negócio.

## Base de referência

Documentos anteriores:

```text
docs/FASE_3_CLASSIFICACAO_FONTES_DADOS.md
docs/FASE_4_AUDITORIA_DEPENDENCIA_EXCEL.md
```

Branch esperada:

```text
limpeza-tests-scripts-checks
```

## Critério de saída

```text
Definição objetiva de:
- quais arquivos compõem o adaptador legado Excel/bridge;
- quais tabelas são staging/temporárias;
- quais tabelas são fonte operacional atual;
- quais tabelas devem ser migradas, renomeadas ou preservadas por compatibilidade;
- fronteira arquitetural proposta entre adaptadores, banco e domínio.
```

## 1. Diagnóstico inicial

A Fase 4 concluiu que:

```text
A dependência direta de Excel está concentrada em db/import_excel.py.
A dependência operacional atual está concentrada em bridge_ingest_csv.py.
A aplicação consome majoritariamente tabelas SQLite, mas essas tabelas ainda carregam semântica e origem de dados do bridge/Excel.
```

## 2. Componentes do adaptador legado

### 2.1 Adaptador legado Excel direto

Arquivo:

```text
db/import_excel.py
```

Responsabilidade atual:

```text
Ler diretamente OPERACOES_E_OPCOES.xlsx e importar abas específicas para tabelas internas.
```

Entrada física:

```text
OPERACOES_E_OPCOES.xlsx
```

Abas críticas:

```text
CONFIGURACOES
ANALISE_ROBO
ANALISE_ROBO_LEGS
HIST_ROBO
ENCERRAMENTOS_MANUAIS
```

Classificação proposta:

```text
Adaptador legado de importação Excel.
Não deve ser considerado camada de domínio.
Não deve ser chamado diretamente por UI, serviços ou repositórios de regra de negócio.
```

### 2.2 Adaptador legado bridge CSV

Arquivo:

```text
bridge_ingest_csv.py
```

Responsabilidade atual:

```text
Ler arquivos CSV exportados pelo bridge e alimentar tabelas SQLite rtd_*.
```

Entrada física:

```text
bridge/*.csv
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

Classificação proposta:

```text
Adaptador legado operacional ativo.
É atualmente o principal acoplamento entre Excel/RTD/bridge e o banco dados/app.db.
```

## 3. Classificação preliminar das tabelas

### 3.1 Tabelas staging/RTD vindas do bridge

Tabelas:

```text
rtd_analise_raiox
rtd_consolidacoes
rtd_analise_robo
rtd_analise_robo_legs
rtd_rolls_detectados
rtd_hist_robo
rtd_encerramentos_manuais
```

Classificação proposta:

```text
Staging operacional de dados externos.
Devem ser tratadas como saída do adaptador bridge, não como modelo canônico definitivo.
```

Observação:

```text
Enquanto o bridge for fonte ativa, essas tabelas podem continuar sendo usadas, mas a dependência deve ficar concentrada em repositórios/adaptadores específicos.
```

### 3.2 Tabelas manuais

Tabelas identificadas:

```text
manual_analise_robo_legs
```

Classificação proposta:

```text
Dados editados ou mantidos pela aplicação.
Candidatas mais fortes a fonte canônica do que as tabelas rtd_*, quando representam decisão/manual override do usuário.
```

Risco:

```text
O nome ainda carrega semântica antiga de ANALISE_ROBO_LEGS.
Pode exigir renomeação futura para um nome de domínio.
```

### 3.3 Tabelas importadas diretamente do Excel

Tabelas associadas ao schema legado:

```text
robo_config
robo_snapshot
robo_legs_snapshot
robo_legs_history
encerramentos_manuais
```

Classificação proposta:

```text
Legado de importação Excel direta.
Devem ser preservadas apenas se ainda houver fluxo ativo que dependa delas.
Caso contrário, devem ser candidatas a depreciação controlada.
```

## 4. Fronteira arquitetural proposta

### 4.1 Camada de adaptadores legados

Responsável por:

```text
- Ler Excel;
- Ler CSVs do bridge;
- Normalizar nomes de colunas;
- Converter tipos e datas;
- Persistir dados externos em tabelas staging;
- Registrar erros de ingestão.
```

Arquivos atuais candidatos:

```text
db/import_excel.py
bridge_ingest_csv.py
utils/leg_normalizers.py
```

Fronteira desejada:

```text
Excel/CSV/bridge não devem aparecer em serviços de domínio, UI ou regras de cálculo.
```

### 4.2 Camada de persistência/repositórios

Responsável por:

```text
- Ler tabelas SQLite;
- Aplicar precedência entre dados manuais e dados RTD;
- Entregar objetos de domínio para serviços;
- Esconder detalhes das tabelas rtd_* da camada de domínio sempre que possível.
```

Arquivos atuais:

```text
repositories/market_snapshot_repository.py
repositories/robo_legs_repository.py
repositories/robo_legs_status_repository.py
```

### 4.3 Camada de domínio/serviços

Responsável por:

```text
- Trabalhar com conceitos de domínio;
- Não conhecer nomes físicos de arquivos;
- Evitar dependência direta de bridge, Excel, CSV ou win32com;
- Consumir objetos ou interfaces vindos dos repositórios.
```

Arquivos observados:

```text
domain/market_snapshot.py
domain/calculation_request.py
services/canonical_pricing_facade.py
services/canonical_input_service.py
```

## 5. Decisões propostas

### 5.1 Excel direto

Decisão preliminar:

```text
db/import_excel.py deve ser mantido como importador legado explícito.
Não deve ser expandido.
Não deve ser usado como fonte operacional principal se o bridge CSV já for o fluxo ativo.
```

Ação futura possível:

```text
Mover ou encapsular em pacote de adapters legado, por exemplo:
adapters/legacy_excel/import_excel.py
```

### 5.2 Bridge CSV

Decisão preliminar:

```text
bridge_ingest_csv.py deve ser tratado como adaptador legado operacional.
```

Ação futura possível:

```text
Mover ou encapsular em pacote de adapters, por exemplo:
adapters/legacy_bridge/ingest_csv.py
```

### 5.3 Tabelas rtd_*

Decisão preliminar:

```text
Tabelas rtd_* são staging operacional.
Podem continuar existindo, mas não devem ser promovidas automaticamente a modelo canônico definitivo.
```

Ação futura possível:

```text
Criar camada de leitura canônica que traduza rtd_* para objetos de domínio.
```

### 5.4 Tabelas manual_*

Decisão preliminar:

```text
Tabelas manual_* representam dado mantido pela aplicação ou override manual.
São candidatas a fonte canônica em fluxos onde o usuário editou ou confirmou dados.
```

Ação futura possível:

```text
Avaliar renomeação semântica futura para nomes de domínio, sem referência a abas Excel.
```

## 6. Plano técnico seguro

### Etapa 1 - Documentar fronteira

```text
Criar esta documentação de Fase 5.
```

### Etapa 2 - Confirmar chamadas reais

```text
Verificar onde db/import_excel.py e bridge_ingest_csv.py são chamados.
```

### Etapa 3 - Confirmar consumo de tabelas

```text
Mapear todos os SELECT/INSERT/UPDATE envolvendo rtd_*, manual_* e tabelas legadas do Excel.
```

### Etapa 4 - Definir nomes canônicos futuros

```text
Propor nomes de domínio para tabelas ou views canônicas.
```

### Etapa 5 - Só depois alterar código

```text
Nenhuma alteração estrutural deve ser feita antes de confirmar a fronteira e os consumidores reais.
```

## 7. Comandos de auditoria recomendados

### Chamadas aos adaptadores legados

```bash
git grep -n "import_excel\|bridge_ingest_csv\|read_excel\|read_csv\|BRIDGE_DIR\|OPERACOES_E_OPCOES"
```

### Consumo das tabelas RTD e manuais

```bash
git grep -n "rtd_analise\|rtd_consolidacoes\|rtd_rolls\|rtd_hist\|rtd_encerramentos\|manual_analise"
```

### Dependências técnicas Excel/COM

```bash
git grep -n "win32com\|Excel.Application\|openpyxl\|xlsx\|xlsm"
```

## 8. Resultado esperado da Fase 5

Ao final da fase, o projeto deve ter uma definição clara:

```text
Excel e bridge são adaptadores legados.
Tabelas rtd_* são staging operacional.
Tabelas manual_* são candidatas a fonte canônica quando representam dado do usuário.
Domínio e serviços não devem depender diretamente de arquivo, bridge, CSV, Excel ou COM.
```

## 9. Próxima fase recomendada

```text
Fase 6 - Criar ou consolidar uma camada canônica de leitura, escondendo nomes rtd_* e manual_* atrás de repositórios/interfaces estáveis.
```
