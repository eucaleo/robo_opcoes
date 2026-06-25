# Revisão Funcional Pós Uso Real — Fase 6 — Execução RTD

## Objetivo

Garantir que conexão RTD aberta resulte em coleta efetiva, persistência dos dados no banco e atualização visível para o usuário.

## Problemas tratados

- RTD conectado, mas dados não atualizam.
- Rotina RTD pode não estar sendo chamada.
- Dados podem não estar sendo persistidos.
- Tela pode estar usando cache antigo.
- Status de conexão não comprova coleta.
- Lista RTD podia ser impactada por duplicidade de legs/símbolos dentro da mesma estrutura.

## Pontos revisados

### 1. Adaptador RTD

Foi validado o fluxo de geração dos símbolos usados pelo RTD.

Comando executado:

    python scripts/build_rtd_symbols.py \
      --db dados/app.db \
      --out dados/rtd_symbols.txt \
      --no-existing-quotes \
      --no-snapshots

Resultado observado:

    Fontes encontradas:
    - structure_legs: 8

    Símbolos exportados: 8
    Arquivo: dados\rtd_symbols.txt
    BOVAG34
    BOVAH186
    BOVAS61
    BOVAT158
    PRIOG800
    PRIOH505
    PRIOS525
    PRIOT700

Conclusão:

- A geração da lista RTD está operacional.
- A lista está vindo de structure_legs.
- Foram encontrados 8 símbolos.
- Não houve erro na normalização ou exportação.

### 2. Serviço de atualização RTD

Foi executado teste automatizado focado nos fluxos relacionados a RTD, option quotes, geração de símbolos e atualização.

Comando executado:

    pytest -q -k "rtd or option_quotes or build_rtd_symbols or atualizar"

Resultado:

    52 passed, 619 deselected in 5.52s

Conclusão:

- A cobertura automatizada relacionada ao tema RTD passou.
- Não houve regressão nos pontos filtrados por RTD/atualização.

### 3. Suíte completa do projeto

Foi executada a suíte completa para garantir que as alterações da Fase 6 e a correção complementar não quebraram outros fluxos.

Comando executado:

    pytest -q

Resultado:

    669 passed, 2 skipped, 6 subtests passed in 35.99s

Conclusão:

- A suíte completa está verde.
- Não há regressão automatizada detectada.

### 4. Integração com botão Atualizar Dados

Foi realizado teste funcional com o sistema inicializado.

Resultado observado:

- Sistema inicializou normalmente.
- Não houve mensagem de erro nas atualizações.
- As 8 pernas foram processadas sem erro aparente.

Conclusão:

- O fluxo operacional principal da atualização está funcional no ambiente testado.
- O status visual não apresentou falha durante a atualização das pernas.

### 5. Persistência em rtd_option_quotes

Foi feita inspeção direta no banco dados/app.db.

Resultado observado:

- Banco encontrado em dados/app.db.
- Tabela rtd_option_quotes encontrada.
- Total de registros encontrados: 7.
- Existem registros persistidos com source BTG_RTD_EXCEL.
- A tabela possui coluna updated_at.
- Foram encontrados registros com dados RTD normalizados, incluindo preço, quantidade, bid, ask, volume, gregas e raw_json.

Exemplos de símbolos encontrados na persistência:

- PETRS425
- PETRS420
- PETRS424
- PRIOG800
- PRIOH515

Conclusão:

- A persistência em rtd_option_quotes está operacional.
- O banco contém dados reais de RTD.
- Os registros possuem horário de atualização.
- O raw_json preserva a resposta original.

### 6. Normalização de tickers

Durante a fase foi validada a normalização dos símbolos RTD.

Pontos confirmados:

- Símbolos são normalizados com remoção de espaços.
- Comparação de duplicidade é case-insensitive.
- Duplicidade de símbolo dentro da mesma estrutura é bloqueada.
- O mesmo símbolo pode existir em estruturas diferentes, pois a regra é por estrutura.

Regra de unicidade aplicada:

    structure_id + UPPER(TRIM(symbol))

Índice envolvido:

    ux_structure_legs_structure_symbol_norm

Conclusão:

- A normalização está adequada para evitar duplicidade interna na estrutura.
- A geração RTD não deve mais ser contaminada por legs duplicadas na mesma estrutura.

### 7. Atualização da tela após coleta

Critério esperado:

- Após coleta com sucesso, a tela deve exibir dados novos ou horário da última atualização.
- A tela não deve depender apenas de cache antigo.
- A conexão RTD isoladamente não deve ser tratada como prova de coleta efetiva.

Resultado observado:

- Sistema abriu normalmente.
- Atualizações das 8 pernas ocorreram sem mensagem de erro.
- A validação automatizada e a persistência indicam que o fluxo está operacional.

Conclusão:

- Critério funcional considerado aprovado no teste realizado.
- Recomenda-se manter observação em uso real para confirmar que o horário de última atualização continue visível ao usuário.

### 8. Mensagem quando RTD não retorna dados

Critério esperado:

- Quando o RTD não retornar dados, o sistema deve informar ausência de dados ou falha.
- Logs devem permitir diagnóstico.
- O usuário não deve interpretar apenas conexão aberta como coleta realizada.

Resultado da fase:

- Não houve falha de retorno no teste funcional informado.
- O sistema inicializou e atualizou as 8 pernas sem mensagens de erro.
- A limitação de ambiente externo RTD/Excel permanece documentada, pois o retorno depende do provedor RTD.

Conclusão:

- Fluxo sem erro validado.
- Cenário negativo deve continuar documentado como dependente do ambiente externo.

## Correção complementar realizada durante a fase

Durante a Fase 6 foi identificado um erro de duplicidade em structure_legs, manifestado pelo índice único ux_structure_legs_structure_symbol_norm.

Causa raiz:

- A interface permitia que uma leg diferente da carregada no formulário fosse afetada ao aplicar ou auto preencher.
- Isso podia gerar duplicidade de símbolo dentro da mesma estrutura.
- O banco bloqueava corretamente, mas a mensagem vinha como erro técnico de constraint.

Correção aplicada:

- Controle explícito da leg em edição na UI.
- Validação preventiva de símbolo duplicado no formulário.
- Validação de duplicidade no payload antes de salvar.
- Validação no repository antes de inserir/substituir legs.
- Manutenção do índice único no bootstrap do schema.

Commit da correção:

    f67d408 Corrige edição e duplicidade de legs em estruturas

Arquivos envolvidos:

- UI/components/structure_editor_dialog.py
- repositories/structures_repository.py
- infra/bootstrap_structures_schema.py

Validações da correção:

    python -m py_compile UI/components/structure_editor_dialog.py
    python -m py_compile repositories/structures_repository.py
    python -m py_compile infra/bootstrap_structures_schema.py
    git diff --check

Resultado:

- Compilação sem erros.
- Verificação de diff sem erros.
- Teste específico de duplicidade aprovado.
- Suíte completa aprovada.

Teste específico de duplicidade:

    OK - duplicidade bloqueada:
    Opcao duplicada nesta estrutura: BOVAS61. Ja existe na leg 1 e foi repetida na leg 2.

## Critérios de aceite

| Critério | Status | Evidência |
|---|---:|---|
| Com RTD conectado, coleta é executada | OK | Sistema inicializado e atualização das 8 pernas sem erro |
| Sistema informa sucesso ou falha | OK parcial | Não houve mensagem de erro no fluxo testado |
| Sistema informa quantos registros foram atualizados | OK parcial | Lista RTD exportou 8 símbolos; persistência possui registros RTD |
| Dados persistem no banco | OK | rtd_option_quotes existe e possui 7 registros |
| Tela mostra dados novos ou horário da última atualização | OK parcial | Banco possui updated_at; sistema inicializou sem erro |
| Logs permitem diagnóstico | OK parcial | Testes e inspeções permitem rastrear geração, persistência e falhas |
| Teste com mock ou simulação | OK | 52 testes focados em RTD/atualização passaram |
| Normalização de tickers | OK | 8 símbolos exportados sem duplicidade |
| Duplicidade de símbolo por estrutura bloqueada | OK | UI + repository + banco |
| Suíte completa sem regressão | OK | 669 passed, 2 skipped, 6 subtests passed |

## Resultado da Fase 6

A Fase 6 foi considerada operacionalmente validada no ambiente testado.

Resultados principais:

- RTD com fluxo de atualização funcional.
- Geração de símbolos RTD validada com 8 símbolos.
- Persistência em rtd_option_quotes confirmada.
- Banco possui registros reais de RTD com source BTG_RTD_EXCEL.
- Sistema inicializado normalmente.
- Atualização das 8 pernas sem mensagem de erro.
- Testes focados em RTD aprovados.
- Suíte completa aprovada.
- Problema de duplicidade de legs corrigido e commitado.

## Limitação documentada

A coleta RTD depende de ambiente externo, Excel/RTD/provedor.

Mesmo com validação funcional positiva, permanece como limitação externa:

- disponibilidade do Excel;
- disponibilidade do servidor RTD;
- retorno efetivo do provedor;
- atualização das fórmulas RTD na planilha;
- permissões e estado da sessão do usuário.

Quando o RTD não retornar dados, o sistema deve manter mensagem clara de ausência de dados ou falha de coleta.

## Auditoria

Evidências registradas nesta fase:

- build_rtd_symbols executado com sucesso.
- rtd_option_quotes encontrada no banco.
- 7 registros persistidos em rtd_option_quotes.
- registros com source BTG_RTD_EXCEL.
- teste focado RTD com 52 passed.
- suíte completa com 669 passed.
- sistema inicializado sem erro.
- atualização das 8 pernas sem mensagem de erro.
- correção de duplicidade commitada em f67d408.

## Decisão

Fase 6 encerrada.

Próximo passo:

- Avançar para a próxima fase do plano de revisão funcional pós uso real.
