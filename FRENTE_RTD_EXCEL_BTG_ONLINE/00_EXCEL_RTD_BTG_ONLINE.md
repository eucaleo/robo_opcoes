# RTD / Excel / BTG Online

## Objetivo

Manter o arquivo `LISTA_RTD.xlsm` aberto junto com o sistema, ajustando a arquitetura para que o Excel funcione como uma antena RTD viva.

Em vez de o sistema chamar scripts para buscar uma opção sob demanda, o Excel passa a receber continuamente os dados da corretora, e o sistema Python passa a consumir esse fluxo.

A decisão arquitetural principal é transformar o RTD em uma fonte contínua de estado e eventos.

## Regras explícitas para desenvolvimento do projeto

1. Não migrar para web.
2. Não utilizar emojis.
3. Manter-se ao escopo do projeto sem derivações.
4. Efetuar buscas de dados e arquivos antes de alterações.
5. Toda mudança deve ser testada após concluída.
6. Após o encerramento de fase, o teste deve compor todas as fases encerradas, para não deixar pendências.
7. Evitar códigos intermediários em explicações, ir direto ao ponto.
8. Em alterações, sempre gerar código automatizado via Git Bash, indentado.
9. A cada alteração concluída e testada, commitar.
10. Não codar sem rumo. Se necessário, buscar a evolução no Git.
11. Criar arquivo de auditoria para ser atualizado com os testes, criando caminho de evolução e auditando o que está pronto.
12. Não gerar dívida técnica. Para cotação viva, isso é risco operacional.

## Visão geral da nova arquitetura

### Programa da corretora

Deve ser aberto primeiro.

Responsabilidades:

- Manter conexão com o provedor RTD da corretora.
- Garantir que os dados estejam disponíveis para o Excel.

### Excel `LISTA_RTD.xlsm`

Deve abrir com o sistema e encerrar com o sistema.

Responsabilidades:

- Ficar aberto durante todo o uso do sistema.
- Receber dados RTD em tempo quase real.
- Manter uma aba viva com ativos, opções, VWAP, bid, ask, último, volume, gregas e demais campos disponíveis.
- Não abrir e fechar a cada consulta.
- Não ser chamado por subprocesso para cada símbolo.

### Sistema Python

Passa a operar com um coletor online.

Responsabilidades:

- Observar o estado vivo do Excel.
- Atualizar o banco de forma controlada.
- Atualizar a UI quase instantaneamente.
- Alimentar estruturas, pernas, payoff, painel operacional e gráficos.

### Banco de dados

Passa a ter dois papéis separados:

- Estado atual dos ativos e opções.
- Histórico temporal para gráficos, candles, VWAP e replay.

## Separação entre snapshot e histórico

### Snapshot atual

Representa apenas o último estado conhecido de cada ativo ou opção.

Características:

- Uma linha por símbolo.
- Atualização por sobrescrita.
- Crescimento controlado.
- Fonte principal da UI.

Usos:

- Preencher legs.
- Atualizar UI.
- Calcular estruturas.
- Mostrar preço atual.
- Mostrar VWAP atual.
- Mostrar bid, ask, spread, volume e gregas atuais.

### Histórico temporal

Representa os pontos gravados ao longo do tempo.

Características:

- Cresce de forma controlada.
- Não deve salvar microvariações infinitamente.
- Deve gravar apenas pontos com valor analítico.

Camadas sugeridas:

- Ticks ou pontos brutos do dia.
- Candles de 1 minuto.
- Candles de 5 minutos.
- Candles de 15 minutos.
- Candles diários.
- Estado final do dia.

## Política de crescimento do banco

### Snapshot atual

- Manter apenas uma linha por símbolo.
- Crescimento limitado.

### Ticks brutos

- Guardar somente o dia atual ou poucos dias.
- Após consolidar em candles, apagar ou arquivar.

### Candles de 1 minuto

- Guardar por período maior.
- Sugestão inicial: 60 ou 90 dias.

### Candles de 5 e 15 minutos

- Guardar por vários meses.
- Sugestão inicial: 1 ano.

### Candles diários

- Guardar indefinidamente.

## Gráficos

A fonte principal do gráfico deve ser o banco de dados, não imagens.

Imagens não devem ser usadas como base histórica porque:

- Não permitem recalcular indicadores.
- Não permitem zoom inteligente.
- Não permitem comparação de estratégias.
- Não permitem refazer candles.
- Não permitem backtest.
- Viram apenas registro visual morto.

O correto é armazenar candles no banco.

## VWAP

Se o BTG fornece apenas o valor atual do VWAP, o sistema deve transformar esse valor em série temporal própria.

Fluxo:

- Excel recebe o VWAP atual.
- Coletor registra VWAP com horário.
- Gráfico exibe linha histórica de VWAP.
- Cada candle pode carregar o VWAP daquele momento.

Análises possíveis:

- Preço acima ou abaixo do VWAP.
- Inclinação do VWAP.
- Distância percentual entre preço e VWAP.
- Cruzamento do preço com VWAP.
- Confirmação por volume.

## Criação de candles a partir dos snapshots

Para cada símbolo, o coletor agrupa pontos por intervalo.

Campos possíveis do candle:

- Abertura.
- Máxima.
- Mínima.
- Fechamento.
- Volume.
- VWAP do período.
- Bid médio ou último bid.
- Ask médio ou último ask.
- Spread médio.
- Quantidade de atualizações.

Exemplo de candle de 1 minuto:

- Primeiro preço do minuto vira abertura.
- Maior preço vira máxima.
- Menor preço vira mínima.
- Último preço vira fechamento.
- Último VWAP ou VWAP médio vira linha VWAP.
- Volume pode ser calculado por diferença, se o campo vier acumulado.

## Camadas sugeridas

### Camada 1: Excel RTD vivo

Responsabilidades:

- Manter conexão com RTD.
- Expor tabela viva com símbolos monitorados.
- Atualizar campos em tempo real ou quase real.

Cuidados:

- Macro habilitada.
- Cálculo automático.
- Excel aberto.
- Corretora conectada.
- Lista de símbolos controlada.

### Camada 2: Coletor RTD online

Responsabilidades:

- Ler periodicamente ou por evento os dados do Excel.
- Detectar alterações.
- Normalizar campos.
- Validar símbolos.
- Atualizar snapshot.
- Enviar eventos para a UI.
- Alimentar histórico intraday.

Decisão inicial:

- Começar dentro do sistema Python.
- Separar em serviço local somente se necessário.

### Camada 3: Banco de snapshot

Responsabilidades:

- Guardar o último estado de cada símbolo.
- Ser rápido.
- Ser simples.
- Servir como fonte principal para a UI.

### Camada 4: Banco histórico intraday

Responsabilidades:

- Guardar pontos temporais relevantes.
- Permitir construção de candles.
- Permitir replay.
- Permitir auditoria.

Regras:

- Gravar somente se houve mudança relevante.
- Ou gravar no máximo uma vez por intervalo.
- Evitar milhares de linhas idênticas.
- Separar ticks brutos de candles consolidados.

### Camada 5: Motor de candles

Responsabilidades:

- Ler pontos históricos.
- Agrupar por tempo.
- Criar candles.
- Atualizar gráfico.
- Consolidar final do dia.

Candles previstos:

- 1 minuto.
- 5 minutos.
- 15 minutos.
- Diário.

### Camada 6: UI em tempo real

Responsabilidades:

- Receber eventos do coletor.
- Atualizar painéis.
- Atualizar legs.
- Atualizar estruturas.
- Atualizar gráficos.
- Evitar redesenho excessivo.

A UI não deve redesenhar tudo a cada microalteração.

## Fluxo operacional sugerido

### Antes de abrir o sistema

- Abrir programa da corretora.
- Confirmar dados atualizando.
- Confirmar RTD ativo.
- Abrir o sistema, que abre o Excel visível ou não, mantendo-o ativo enquanto o sistema estiver aberto.

### Ao abrir o sistema

- Verificar se o Excel está aberto.
- Verificar se a planilha correta está aberta.
- Verificar se a aba RTD está disponível.
- Verificar se os campos obrigatórios existem.
- Iniciar coletor online.
- Carregar snapshot atual.
- Começar atualização da UI.

### Durante o pregão

- RTD atualiza Excel.
- Coletor lê mudanças.
- Snapshot é atualizado.
- Histórico recebe pontos relevantes.
- Motor de candles consolida intervalos.
- UI atualiza painéis e gráficos.
- Estruturas são recalculadas.

### Ao encerrar o sistema

- Consolidar candles finais.
- Salvar estado do dia.
- Limpar ticks brutos antigos, se aplicável.
- Manter snapshots finais.
- Manter histórico consolidado.

Se necessário, o encerramento pode ser atrasado para concluir coleta e consolidação.

## Fonte do preço do candle

Regras iniciais:

- Para ativo líquido: usar último negócio.
- Para opção pouco líquida: usar mid price entre bid e ask.
- Para decisão de compra: olhar ask e VWAP.
- Para decisão de venda: olhar bid e VWAP.
- Para gráfico operacional: permitir escolher a fonte.

## Frequência de captura

Regras iniciais:

- Snapshot: atualizar sempre que detectar mudança.
- Histórico bruto: gravar no máximo uma vez por segundo por símbolo, salvo mudança relevante.
- Candles: consolidar por minuto.
- UI: atualizar algumas vezes por segundo, não a cada célula alterada.

## Símbolos monitorados

Não monitorar o mercado inteiro sem necessidade.

Monitorar:

- Ativo base principal.
- Opções das estruturas abertas.
- Opções favoritas.
- Lista operacional do dia.
- Símbolos adicionados pela UI.

## Retenção histórica

Política inicial:

- Ticks brutos: poucos dias.
- Candles de 1 minuto: 60 ou 90 dias.
- Candles de 5 minutos: 1 ano.
- Candles diários: indefinidamente.

## Falhas previstas

O sistema deve prever:

- Excel fechado sem querer.
- Corretora desconectada.
- RTD parado.
- Planilha congelada.
- Células com erro.
- Campo vazio.
- Horário fora do pregão.

A UI deve mostrar:

- RTD online.
- Excel aberto.
- Corretora conectada.
- Última atualização.
- Quantidade de símbolos ativos.
- Símbolos com erro.
- Atraso dos dados.

Adicionar no menu Ajuda um botão que mostre o resumo da conexão com os dados.

## Riscos e cuidados

### Excel pode virar gargalo

Cuidados:

- Não exagerar no número de símbolos.
- Evitar fórmulas pesadas.
- Evitar macros rodando a cada célula sem controle.
- Usar leitura em bloco, não célula por célula.
- Ter botão ou rotina de reconexão.

### SQLite pode travar se escrever demais

Cuidados:

- Usar snapshot por sobrescrita.
- Gravar histórico com redução inteligente.
- Consolidar candles.
- Evitar commit para cada célula.
- Usar fila de gravação.
- Usar modo adequado para escrita concorrente.

### UI pode ficar pesada

Cuidados:

- Separar coleta de dados da renderização.
- Atualizar gráfico em intervalos controlados.
- Atualizar apenas o símbolo visível.
- Atualizar apenas estruturas abertas.
- Evitar recalcular tudo sem necessidade.

### Candle de opção pode ser ruidoso

Cuidados:

- Usar mid price quando não houver negócio.
- Marcar no gráfico qual fonte está sendo usada.
- Diferenciar candle real de candle sintético.
- Exibir spread junto.
- Não tomar decisão apenas pelo candle se o book estiver ruim.

## Plano em fases

### Fase 1: Transformar RTD em fonte online

Objetivo:

Ter o sistema lendo dados vivos do Excel.

Itens:

- Manter `LISTA_RTD.xlsm` aberto.
- Criar mecanismo de detecção do Excel aberto.
- Ler tabela viva do RTD.
- Atualizar snapshot no banco.
- Exibir status RTD na UI.
- Eliminar necessidade de subprocesso para preencher leg.

### Fase 2: Snapshot centralizado

Objetivo:

Deixar o sistema mais rápido e mais simples.

Itens:

- Criar tabela de estado atual por símbolo.
- Atualizar por sobrescrita.
- Normalizar campos em uma única camada.
- Fazer pernas e estruturas lerem dessa tabela.
- Botão "Preencher por RTD" passa a usar snapshot.

### Fase 3: Histórico intraday

Objetivo:

Começar a formar a base dos gráficos.

Itens:

- Criar armazenamento temporal dos pontos relevantes.
- Gravar timestamp, símbolo, preço, VWAP, bid, ask, volume e demais campos.
- Controlar frequência de gravação.
- Evitar crescimento exagerado.

### Fase 4: Motor de candles

Objetivo:

Fazer o gráfico funcionar sem depender de gráfico pronto do BTG.

Itens:

- Criar candles a partir dos pontos capturados.
- Gerar candles de 1 minuto.
- Gerar candles de 5 e 15 minutos.
- Associar VWAP ao candle.
- Exibir candles no gráfico atual.

### Fase 5: UI operacional em tempo real

Objetivo:

Transformar a tela em terminal operacional vivo.

Itens:

- Atualizar painel de opções.
- Atualizar legs.
- Atualizar estruturas.
- Atualizar gráfico.
- Mostrar VWAP, preço, spread e decisão.
- Mostrar status de atualização.

### Fase 6: Retenção, limpeza e consolidação

Objetivo:

Evitar crescimento infinito e manter performance.

Itens:

- Consolidar candles no fim do dia.
- Limpar ticks brutos antigos.
- Manter candles históricos.
- Criar rotina de manutenção do banco.
- Criar compactação periódica, se necessário.

### Fase 7: Alertas e decisão operacional

Objetivo:

Usar os dados vivos para tomada de decisão, não apenas visualização.

Itens:

- Criar regras de decisão com VWAP.
- Alertar cruzamento de preço com VWAP.
- Alertar spread anormal.
- Alertar liquidez baixa.
- Alertar estrutura favorável.
- Alertar mudança relevante no payoff.

## Arquitetura final recomendada

A solução recomendada:

- Excel aberto o tempo todo como receptor RTD.
- Sistema Python com coletor online interno.
- Snapshot em banco para estado atual.
- Histórico intraday separado.
- Candles gerados pelo próprio sistema.
- VWAP tratado como linha histórica capturada.
- UI atualizada por eventos e com limite de redesenho.
- Sem subprocesso para consultar opção individual.
- Subprocessos apenas para manutenção, importação ou recuperação emergencial.

## Resumo da decisão

A arquitetura online é melhor do que a arquitetura sob demanda.

Caminho correto:

- Não pedir dado ao RTD toda hora.
- Deixar o RTD alimentar o Excel continuamente.
- Usar o Excel como ponte viva.
- O sistema observa, normaliza, grava e desenha.
- Snapshot para velocidade.
- Histórico para análise.
- Candles para gráfico.
- VWAP como série temporal capturada internamente.

Ganhos esperados:

- Velocidade.
- Menos complexidade operacional.
- Menos subprocessos.
- Menos espera.
- UI online.
- Estruturas online.
- Gráficos possíveis.
- Histórico útil.
- Base para replay e alertas.
- Melhor uso real do VWAP.
