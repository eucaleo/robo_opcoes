# Guia de Desenvolvimento - BD Único app.db

## Objetivo da frente

Eliminar o banco dados/derived.db como banco físico do sistema e absorver todas as suas responsabilidades válidas dentro de dados/app.db.

A arquitetura final será:

dados/app.db = único banco físico do sistema.

O sistema não terá mais dados/derived.db como banco físico, origem, destino, cache separado, fallback, banco auxiliar ou banco de sincronização.

## Decisão arquitetural final

O sistema passa a operar com apenas um banco:

dados/app.db

Este banco será responsável por:

- Mercado vivo
- RTD de opções
- RTD de ativo objeto
- UI
- Pricing runtime
- Payoff
- Simulações
- Caches
- Resultados derivados
- Artefatos regeneráveis
- Market snapshot, se existir e for usado
- Qualquer função ainda válida que antes dependia de dados/derived.db

## Situação perigosa que será eliminada

Hoje existe ou pode existir duplicidade operacional entre:

app.db.rtd_option_quotes
derived.db.rtd_option_quotes

app.db.rtd_underlying_quotes
derived.db.rtd_underlying_quotes

Essa situação será eliminada.

A fonte oficial será somente:

dados/app.db

## Regra principal da frente

Não vamos apenas apagar dados/derived.db.

Vamos eliminar o banco físico dados/derived.db e migrar para dados/app.db toda responsabilidade funcional ainda válida que dependia dele.

Portanto:

rtd_option_quotes passa a existir e operar somente em dados/app.db.
rtd_underlying_quotes passa a existir e operar somente em dados/app.db.
Payoff, simulações, caches, resultados derivados e artefatos regeneráveis passam a operar em dados/app.db.
Nenhum fluxo pode criar, consultar ou depender de dados/derived.db.

## Regras explícitas para desenvolvimento

A) Não migrar para web.

B) Não utilizar emojis.

C) Manter-se ao escopo do projeto sem derivações.

D) Efetuar buscas de dados e arquivos antes de alterações.

E) Toda mudança deve ser testada após concluída.

F) Após o encerramento de fase, o teste deve compor todas as fases encerradas, para não ficarem pendências.

G) Evitar códigos intermediários em explicações. Ir direto ao ponto.

H) Em alterações, sempre gerar código automatizado via Git Bash indentado.

I) Comitar fases concluídas.

J) Não codar sem rumo. Se necessário, buscar a evolução no Git.

K) Criar arquivo de auditoria para ser atualizado com os testes, conclusões e caminho de evolução.

L) Não criar arquivos com blocos de crase no conteúdo.

M) Não manter sincronização contínua derived.db para app.db.

N) Não manter sincronização app.db para derived.db.

O) Não permitir dívida técnica. Para cotação viva isso é risco operacional.

P) Após testes, a arquitetura final aceita será um único banco físico: dados/app.db.

## Proibições da frente

Fica proibido manter ou criar:

- dados/derived.db
- referência ativa a derived.db
- banco físico auxiliar para dados derivados
- fallback para derived.db
- sincronização derived.db para app.db
- sincronização app.db para derived.db
- criação automática de derived.db
- testes que dependam de derived.db
- inicializadores que criem derived.db
- constantes de caminho para derived.db
- funções como get_derived_db_path, se existirem
- qualquer leitura ou gravação operacional em derived.db

## O que deve ser absorvido pelo app.db

Tudo que ainda for funcionalmente necessário e hoje depender de derived.db deverá ser migrado para app.db.

Exemplos:

Origem antiga:
derived.db.payoff_*

Destino novo:
app.db.payoff_*

Origem antiga:
derived.db.simulation_*

Destino novo:
app.db.simulation_*

Origem antiga:
derived.db.cache_*

Destino novo:
app.db.cache_*

Origem antiga:
derived.db.derived_*

Destino novo:
app.db.derived_*

Origem antiga:
derived.db.market_snapshot_*, se existir e for usado

Destino novo:
app.db.market_snapshot_*

## Fase 0 - Inventário obrigatório

Antes de qualquer alteração funcional, buscar tudo na raiz do projeto.

Buscar por:

- derived.db
- app.db
- derived_repo
- derived_service
- tabelas derivadas
- payoff
- simulações
- caches
- RTD
- market snapshot
- conexões SQLite
- sqlite3.connect
- db_path
- database_path
- inicializadores de schema
- testes

Objetivo:

Saber exatamente o que depende de dados/derived.db e o que precisa ser absorvido por dados/app.db.

## Fase 1 - Classificação funcional

Cada ocorrência encontrada no inventário deve ser classificada.

Classes e decisões:

Função ainda necessária:
Migrar para app.db.

Tabela ainda necessária:
Criar ou manter no schema do app.db.

Código de sincronização:
Remover.

Fallback para derived.db:
Remover.

Inicialização de derived.db:
Remover.

Teste antigo:
Corrigir para app.db.

Documentação ativa:
Atualizar.

Documentação histórica:
Manter somente se não induzir desenvolvimento errado.

## Fase 2 - Migração de schema para app.db

Tudo que for necessário do antigo derived.db deve passar a existir dentro do app.db.

Objetivo:

Garantir que app.db possua o schema necessário para absorver:

- payoff
- simulações
- caches
- resultados derivados
- market snapshot, se usado
- qualquer tabela derivada necessária
- RTD de mercado vivo

Sem criar banco intermediário.

Sem usar derived.db como etapa temporária.

Sem sync.

## Fase 3 - Migração dos repositórios e serviços

Alterar código para que os componentes passem a usar app.db.

Comportamento esperado:

derived_repo.py:
Se ainda existir, deve conectar em app.db.

derived_service.py:
Se ainda existir, deve usar tabelas dentro de app.db.

payoff:
Deve ler e gravar em app.db.

simulações:
Devem ler e gravar em app.db.

caches derivados:
Devem ler e gravar em app.db.

market snapshot:
Deve ler e gravar em app.db, se existir e for usado.

RTD:
Deve continuar exclusivamente em app.db.

## Fase 4 - Remoção do banco separado

Eliminar:

- constante de caminho para derived.db
- função get_derived_db_path
- inicializador de derived.db
- criação automática de dados/derived.db
- fallback para derived.db
- sync entre bancos
- testes que montam derived.db
- fixtures que criam derived.db
- documentação ativa que oriente uso de derived.db

Como foi definido sem backup, não haverá etapa de preservação do banco derived.db.

## Fase 5 - Testes obrigatórios

Criar testes para garantir que a decisão não volte a quebrar.

Teste 1:
Proibição estática de derived.db.

Validações:

- derived.db não aparece em código produtivo
- dados/derived.db não aparece em código produtivo
- não existe get_derived_db_path
- não existe DERIVED_DB_PATH
- não existe fallback para derived.db

Teste 2:
app.db como único banco.

Validações:

- o caminho canônico do banco é dados/app.db
- repositórios principais usam app.db
- serviços de leitura usam app.db
- serviços de escrita usam app.db

Teste 3:
RTD no app.db.

Validações:

- rtd_option_quotes pertence ao app.db
- rtd_underlying_quotes pertence ao app.db
- runtime lê RTD do app.db
- runtime não tenta derived.db

Teste 4:
Derivados no app.db.

Validações:

- payoff grava ou lê no app.db
- simulações gravam ou leem no app.db
- caches derivados gravam ou leem no app.db
- nenhum desses fluxos cria derived.db

Teste 5:
Não criação física de derived.db.

Validações:

- executar inicializadores não cria dados/derived.db
- executar fluxo de pricing não cria dados/derived.db
- executar fluxo de payoff não cria dados/derived.db
- executar fluxo de market snapshot não cria dados/derived.db

Teste 6:
Absorção funcional do antigo derived.db.

Validações:

- tabelas necessárias do antigo derived.db existem no app.db
- repositórios derivados usam app.db
- serviços derivados usam app.db
- fluxos principais passam sem derived.db
- após execução, dados/derived.db não existe

## Fase 6 - Execução cumulativa de testes

A cada fase encerrada, os testes novos devem ser executados.

Comandos previstos:

python -m pytest ATT/tests/test_bd_unico_no_derived_db_contract.py -q
python -m pytest ATT/tests/test_bd_unico_app_db_contract.py -q
python -m pytest ATT/tests/test_bd_unico_rtd_tables_app_db.py -q
python -m pytest ATT/tests/test_bd_unico_derived_artifacts_in_app_db.py -q
python -m pytest ATT/tests/test_bd_unico_no_physical_derived_db_creation.py -q
python -m pytest ATT/tests/test_bd_unico_absorcao_funcional.py -q
python -m pytest ATT/tests -q

Se algum teste antigo ainda esperar derived.db, ele deve ser corrigido.

Não marcar como skip para esconder dívida técnica.

## Fase 7 - Auditoria da frente

A auditoria deve ser atualizada a cada fase com:

- fase executada
- objetivo
- buscas realizadas
- arquivos encontrados
- arquivos alterados
- decisões tomadas
- testes criados
- testes executados
- resultado dos testes
- pendências
- commit da fase

Arquivo de auditoria:

FRENTE_BD_UNICO_APPDB/AUDITORIA.md

## Critérios de aceite final

A frente só estará concluída se todos os critérios abaixo forem verdadeiros:

Banco físico único:
dados/app.db

dados/derived.db:
Eliminado.

Criação automática de derived.db:
Não existe.

Fallback para derived.db:
Não existe.

Sync entre bancos:
Não existe.

RTD de opções:
dados/app.db

RTD de ativo objeto:
dados/app.db

UI:
dados/app.db

Pricing runtime:
dados/app.db

Payoff:
dados/app.db

Simulações:
dados/app.db

Caches:
dados/app.db

Artefatos derivados:
dados/app.db

Testes usando derived.db:
Corrigidos.

Testes novos:
Criados.

Testes cumulativos:
Passando.

Auditoria:
Atualizada.

Commit:
Realizado por fase concluída.

## Resultado final esperado

A arquitetura final será:

Um único banco físico para todo o sistema:

dados/app.db

O banco dados/derived.db será eliminado.

As funções válidas antes dependentes de derived.db serão absorvidas por app.db.

Não haverá sincronização entre bancos.

Não haverá fallback.

Não haverá dívida técnica em cotação viva.

