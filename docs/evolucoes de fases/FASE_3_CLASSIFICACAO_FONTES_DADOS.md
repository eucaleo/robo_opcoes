# Fase 3 - Classificação das Fontes de Dados

## Objetivo

Classificar as fontes de dados atuais do sistema conforme a ROTA MESTRE.

Esta fase não altera regra de negócio. O objetivo é separar as fontes em:

```text
entrada bruta
configuração
legado
derivado
operacional
temporário
descartável
```

## Base de referência

Documento anterior:

```text
docs/FASE_2_DIAGNOSTICO_FLUXO_ATUAL.md
```

Branch:

```text
limpeza-tests-scripts-checks
```

Commit de referência:

```text
6167c32 Documenta diagnostico do fluxo atual da fase 2
```

## Critério de saída

```text
Cada fonte classificada com destino claro.
```

## 1. Classificação geral

### Entrada bruta

Fontes classificadas como entrada bruta:

```text
OPERACOES_E_OPCOES.xlsm
CSV exportado da aba RTD_LINKS
cotações RTD de opções
dados de mercado externos
```

Destino:

```text
Devem continuar sendo tratadas como origem externa ou bruta.
Não devem ser consideradas fonte canônica operacional.
Devem alimentar repositórios, snapshots ou processos de normalização.
```

Justificativa:

```text
São fontes externas ao núcleo persistido do sistema.
Podem mudar de formato, depender de Excel, RTD, exportação manual ou captura externa.
```

### Configuração

Fontes classificadas como configuração:

```text
aba CONFIGURACOES do workbook
parâmetros de execução
parâmetros usados por serviços e scripts operacionais
```

Destino:

```text
Devem permanecer separadas de dados operacionais e derivados.
Quando necessário, podem ser migradas para estrutura própria de configuração.
```

Justificativa:

```text
Configuração define comportamento do sistema, mas não representa operação, preço calculado ou snapshot de mercado.
```

### Operacional

Fontes classificadas como operacional:

```text
dados/app.db
structures
structure_legs
cadastro de estruturas
pernas cadastradas em estruturas
```

Módulos principais:

```text
repositories/structures_repository.py
api/structures_controller.py
UI/components/structures_list_panel.py
UI/components/structure_editor_dialog.py
services/canonical_input_service.py
services/canonical_pricing_facade.py
```

Destino:

```text
Devem ser preservadas como fonte operacional principal.
O cadastro novo de estruturas deve continuar usando app.db via StructuresRepository.
```

Justificativa:

```text
Representam o estado operacional persistido do sistema.
São usadas para cadastro, edição, listagem, consulta e formação de entrada canônica.
```

### Legado

Fontes classificadas como legado:

```text
rtd_analise_robo_legs
manual_analise_robo_legs
rtd_analise_robo
bridge/analise_robo.csv
bridge/analise_robo_legs.csv
bridge/analise_raiox.csv
ANALISE_ROBO_LEGS
ANALISE_ROBO
ANALISE_RAIOX
HIST_ROBO
bridge/hist_robo.csv
```

Módulos relacionados:

```text
repositories/market_snapshot_repository.py
repositories/robo_legs_repository.py
repositories/robo_legs_status_repository.py
services/market_snapshot_selector.py
services/robo_legs_service.py
services/legacy_robo_legs_fallback.py
```

Destino:

```text
Devem ser mantidas apenas enquanto forem necessárias para compatibilidade.
Não devem receber novas regras de negócio.
Devem ser isoladas atrás de serviços, seletores ou adaptadores.
Devem ser candidatas a substituição progressiva por fontes operacionais ou derivadas.
```

Justificativa:

```text
Ainda existem dependências de tabelas e artefatos com semântica ANALISE_ROBO.
Essas fontes não devem ser confundidas com o cadastro operacional novo.
```

### Derivado

Fontes classificadas como derivado:

```text
dados/derived.db
resultados de pipeline derivado
payoff calculado
features calculadas
métricas agregadas
```

Módulos relacionados:

```text
domain/payoff.py
domain/payoff_features.py
db/derived_repo.py
db/reader.py
db/writer.py
run_derived_pipeline.py
validate_derived_db.py
```

Destino:

```text
Devem ser tratadas como dados recalculáveis.
Não devem ser fonte primária de cadastro.
Podem ser apagadas e reconstruídas desde que a entrada operacional e bruta exista.
```

Justificativa:

```text
São produtos de cálculo, processamento ou enriquecimento.
Não representam a origem canônica da operação.
```

### Temporário

Fontes classificadas como temporário:

```text
arquivos intermediários de execução local
saídas transitórias de scripts
artefatos gerados durante validações
caches locais não versionados
```

Destino:

```text
Não devem ser versionados.
Devem ser removíveis sem perda de informação operacional.
Devem ser ignorados ou recriados por scripts quando necessário.
```

Justificativa:

```text
Servem apenas para execução, diagnóstico ou validação momentânea.
```

### Descartável

Fontes classificadas como descartável:

```text
arquivos antigos de teste não usados
rascunhos manuais
duplicidades históricas
artefatos residuais de limpeza
saídas obsoletas sem consumidor ativo
```

Destino:

```text
Devem ser removidas quando identificadas com segurança.
Não devem ser usadas como fallback.
Não devem ser documentadas como fonte ativa.
```

Justificativa:

```text
Não têm papel operacional, derivado, bruto ou configuracional claro.
Mantê-las aumenta ambiguidade e risco de regressão.
```

## 2. Classificação por artefato identificado

| Fonte | Classe | Destino |
|---|---|---|
| `dados/app.db` | operacional | fonte principal para cadastro e estado operacional |
| `dados/derived.db` | derivado | base recalculável de resultados derivados |
| `structures` | operacional | manter como cadastro operacional |
| `structure_legs` | operacional | manter como pernas cadastradas da estrutura |
| `rtd_analise_robo_legs` | legado | isolar e substituir progressivamente |
| `manual_analise_robo_legs` | legado | isolar e substituir progressivamente |
| `rtd_analise_robo` | legado | isolar e substituir progressivamente |
| `rtd_option_quotes` | entrada bruta | tratar como cotação importada/normalizada |
| `bridge/analise_robo.csv` | legado | manter apenas enquanto houver consumidor |
| `bridge/analise_robo_legs.csv` | legado | manter apenas enquanto houver consumidor |
| `bridge/analise_raiox.csv` | legado | manter apenas enquanto houver consumidor |
| `bridge/hist_robo.csv` | legado | manter apenas como referência histórica ou migração pontual |
| `HIST_ROBO` | legado | não usar como fonte viva do sistema |
| `OPERACOES_E_OPCOES.xlsm` | entrada bruta/configuração | separar dados de mercado, operação e parâmetros |
| `CONFIGURACOES` | configuração | manter separado de dados operacionais |
| `run_derived_pipeline.py` | operacional de processamento | manter como script autorizado |
| `validate_derived_db.py` | operacional de validação | manter como script autorizado |

## 3. Decisões de classificação

### Decisão 1

```text
O app.db é a base operacional principal.
```

Motivo:

```text
As estruturas novas e persistidas já usam StructuresRepository com persistência em app.db.
```

### Decisão 2

```text
O derived.db é derivado e recalculável.
```

Motivo:

```text
Ele é validado e produzido por pipeline próprio, não sendo origem primária de cadastro.
```

### Decisão 3

```text
As fontes ANALISE_ROBO são legado.
```

Motivo:

```text
Ainda existem tabelas e CSVs com semântica histórica de ANALISE_ROBO_LEGS e ANALISE_ROBO.
Essas fontes devem ser isoladas até serem substituídas.
```

### Decisão 4

```text
Cotações RTD e exportações da aba RTD_LINKS são entrada bruta.
```

Motivo:

```text
São insumos externos de mercado, sujeitos a variação e importação.
```

### Decisão 5

```text
Arquivos temporários e residuais não devem ser versionados.
```

Motivo:

```text
A limpeza residual já valida que não há arquivos temporários antigos ou proibidos versionados.
```

## 4. Destino consolidado

```text
entrada bruta     -> importar, normalizar e não usar como cadastro canônico
configuração      -> manter separada e controlada
operacional       -> preservar como fonte principal de estado do sistema
legado            -> isolar, manter compatibilidade e substituir progressivamente
derivado          -> recalcular a partir das fontes válidas
temporário        -> não versionar e permitir remoção
descartável       -> remover quando identificado com segurança
```

## 5. Próxima fase sugerida

```text
Fase 4 - Auditoria de Dependência do Excel
```

Objetivo esperado:

```text
Descobrir exatamente onde o sistema ainda depende das abas do Excel, CSVs derivados antigos, leituras diretas da bridge e cálculos prontos vindos da planilha.
```

## Conclusão

A classificação das fontes de dados foi concluída.

Resultado:

```text
Cada fonte identificada na Fase 2 possui uma classe e um destino claro.
```

Esta fase não alterou regra de negócio, código de produção, testes ou estrutura de banco.
