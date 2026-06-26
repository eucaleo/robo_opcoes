# Fase 7 — Normalização temporal e estabilização de snapshots derivados

Data de encerramento: 2026-06-25  
Status: **Concluída**

## Objetivo

Normalizar o tratamento de datas e horários no sistema, principalmente nos fluxos de:

- snapshots derivados;
- decisões de estrutura;
- pontos de payoff;
- painel de detalhes;
- grid de decisões;
- exibição de datas na UI.

A fase foi motivada pela identificação de inconsistências entre os campos created_at e timestamp, onde parte dos registros estava gravada sem timezone explícito, parte com +00:00 e parte com -03:00.

## Problema identificado

Antes da correção, o banco continha timestamps em formatos mistos:

- created_at sem timezone explícito;
- timestamp em horário local com -03:00;
- alguns registros antigos com UTC +00:00;
- ordenações usando comparação textual ou COALESCE(created_at, timestamp).

Isso causava risco de:

- exibição com diferença aparente de horário;
- mistura de snapshots antigos e novos;
- seleção incorreta do snapshot mais recente;
- inconsistência visual entre painel de detalhes e grid;
- comportamento instável na atualização da tela.

## Solução implementada

Foi criado o utilitário central:

    core/datetime_utils.py

Esse utilitário passou a concentrar as funções responsáveis por:

- obter horário local timezone-aware;
- gerar ISO 8601 com offset explícito;
- interpretar strings antigas e novas;
- formatar datas para exibição local.

Regra adotada nesta fase:

    Datas novas devem ser gravadas com timezone explícito America/Sao_Paulo.
    Datas antigas sem timezone são interpretadas como America/Sao_Paulo.
    Datas com offset explícito são convertidas corretamente para America/Sao_Paulo na UI.

## Arquivos principais alterados

- core/datetime_utils.py
- db/derived_repo.py
- UI/main_window.py
- UI/components/details_panel.py
- UI/components/decisions_grid.py
- services/derived_service.py

## Correções aplicadas

### 1. Centralização de data/hora

Foi criado um ponto único para parse, normalização e formatação de datas.

### 2. Escrita timezone-aware

Foram substituídos usos diretos de geração de ISO sem timezone por função central com timezone explícito.

Exemplo do padrão antigo identificado:

    datetime.now().isoformat()

Padrão atual esperado:

    now_local_iso()

### 3. UI com formatação local centralizada

A UI deixou de depender de cortes simples de string para exibir datas e passou a usar função central de formatação.

### 4. Ordenação temporal mais segura

Consultas passaram a priorizar ordenação temporal baseada em timestamp interpretável pelo SQLite.

Padrão usado:

    ORDER BY datetime(timestamp) DESC

### 5. Payoff usando snapshot mais recente

O painel de detalhes passou a buscar os pontos de payoff somente do timestamp mais recente da estrutura, evitando mistura de recálculos antigos e novos.

## Evidência de validação

Consulta final em dados/derived.db mostrou registros novos normalizados:

    created_at_raw   : 2026-06-25T21:33:14.048166-03:00
    timestamp_raw    : 2026-06-25T21:33:14.018263-03:00
    created_at_local : 2026-06-25 21:33:14
    timestamp_local  : 2026-06-25 21:33:14

Registros antigos sem timezone também foram interpretados corretamente:

    created_at_raw   : 2026-06-25T21:22:21.774831
    timestamp_raw    : 2026-06-25T21:22:21.745047-03:00
    created_at_local : 2026-06-25 21:22:21
    timestamp_local  : 2026-06-25 21:22:21

## Validação por grep

Foi executada uma busca por usos diretos ou defaults potencialmente problemáticos:

    datetime.utcnow
    utcnow
    datetime.now().isoformat()
    CURRENT_TIMESTAMP
    datetime('now')

Resultado: não foram encontrados usos problemáticos em fluxo direto principal de gravação.

Ocorrências restantes foram identificadas em definições de schema:

    db/derived_repo.py
    db/schema.py
    db/schema_excel.py

Essas ocorrências foram classificadas como pendência técnica não bloqueante, pois os fluxos principais passaram a fornecer timestamp explícito.

## Resultado operacional

Após a fase:

- a atualização da UI ficou mais estável;
- a tela apresentou melhora perceptível de desempenho;
- novos snapshots passaram a gravar datas com offset explícito;
- a visualização passou a ser consistente;
- o pipeline finalizou com sucesso;
- snapshots foram validados como consistentes.

## Pendências técnicas registradas

Para fase futura:

1. Avaliar remoção ou substituição de DEFAULT CURRENT_TIMESTAMP e datetime('now') nos schemas.
2. Decidir se os registros antigos devem ser migrados fisicamente para ISO com offset explícito.
3. Padronizar política definitiva entre:
   - gravar tudo em UTC;
   - ou gravar tudo em America/Sao_Paulo com offset explícito.

Na Fase 7, foi adotada a abordagem com America/Sao_Paulo por compatibilidade com o uso atual e com a visualização esperada pelo usuário.

## Critério de aceite

A Fase 7 é considerada concluída porque:

- registros novos estão timezone-aware;
- registros antigos são lidos corretamente;
- UI usa formatter central;
- payoff usa snapshot mais recente;
- pipeline executa com sucesso;
- compilação não apresentou erro;
- validação manual confirmou equivalência entre created_at e timestamp na visualização local.

## Commit principal

    c106780 Normaliza datas timezone-aware na UI e snapshots derivados

