ROTA_REVISAO_FUNCIONAL_POS_USO_REAL
REVISAO DE FUNCIONALIDADES

Importante a todos os projetos e fases:

A)	Não migrar para web
B)	Não utilizar emojis
C)	Manter-se ao scopo do projeto sem derivações
D)	Efetuar buscas de dados e arquivos antes de alterações 
E)	Toda mudança deve ser testada apos concluida
F)	Apos o encerramento de fase o teste deve compor todas as fases encerradas, assim não ficara pendencias
G)	Evitar codigos intermediarios em explicações, ir direto ao ponto
H)	Em alterações sempre gerar codigo inteiro do arquivo
I)	A cada alteração concluida e testada, commitar.
J)	Não codar sem rumo, se necessario buscar a evolução no git
K)	Criar arquivo de auditoria pra ser atualizado com os testes, assim vamos testando as conclusoes e criando o caminho de evolução ao mesmo tempo auditando o que esta pronto
L)	Não gerar codigo com crase, sempre com identação

Marco 0 —Controle e Congelamento da Rota
Objetivo
Travar a nova estratégia antes de continuar o desenvolvimento.
Escopo
Consolidar a ROTA_REVISAO_FUNCIONAL_POS_USO_REAL como documento norteador atualizado.
Decisões fixadas
•	Excel é apenas ponte RTD.
•	Banco de dados é a fonte da verdade.
•	UI não deve depender de CSVs derivados antigos.
•	Cálculos efetuados todos pelo sistema.
•	Novas estruturas devem nascer no sistema
________________________________________


ERROS ENCONTRADOS NA 1º EXECUÇÃO

1-	Erro ao adicionar manualmente uma estrutura (strike most be numeric) não aceita virgula como separador decimal, aceitando apenas ponto
2-	Mudar funcionalidade de inclusão para modelo assistido, em que o usuário informa os campos principais da operação e o sistema preenche automaticamente os demais dados a partir do símbolo da opção.
3-	Estrutura incluída aparece no sistema, mas curva de payoff não funciona e busca de decisões  também não.
4-	Ao clicar em atualizar dados, o comportamento observado é inconsistente ou insuficiente: em alguns casos há mensagem genérica de sucesso, mas sem detalhar o que foi executado, quantos registros foram processados, se houve RTD, payoff ou decisões geradas.
5-	Não executou atualizações RTD (conexão aberta)

Revisao de Funcionalidades

Objetivo
Registrar problemas encontrados durante o uso real do sistema e definir uma rota organizada de correcao, validacao e fechamento, sem perder o rumo do desenvolvimento.
Esta revisao parte da branch main limpa apos o encerramento da ROTA_MESTRE_3.

Estado inicial
Branch base:
 main
Ultimo marco conhecido:
ROTA_MESTRE_3 encerrada
    	main sincronizada com origin/main
    	commit de fechamento: f95bcb8

Problemas identificados
1. Erro ao adicionar manualmente uma estrutura com valores usando virgula

Sintoma
Ao adicionar manualmente uma estrutura, o sistema apresenta erro semelhante a:
(strike must be numeric) O sistema aceita valores com ponto decimal, por exemplo:   10.50 
mas nao aceita valores com virgula decimal, por exemplo:
	10,50
Impacto
No contexto brasileiro, o usuario tende a informar valores decimais usando virgula. Isso gera erro de validacao e impede o cadastro manual adequado.
Hipotese inicial
A validacao numerica esta usando conversao direta para float ou decimal sem normalizacao previa do formato brasileiro.
Correcao esperada
Antes da validacao numerica, o sistema deve normalizar entradas monetarias e numericas aceitando:
      10,50
    	      10.50
    	1.234,56
    	1234,56
    	1234.56
O valor final interno deve ser convertido para formato numerico padrao do sistema.
Pontos a revisar
- Formularios de inclusao manual de estrutura.
- Validadores de strike.
- Validadores de preco.
- Conversores de campos numericos.
- Mensagens de erro exibidas ao usuario.
Criterios de aceite
- O sistema deve aceitar strike informado com virgula decimal.
- O sistema deve aceitar strike informado com ponto decimal.
- O sistema nao deve aceitar texto invalido.
- A mensagem de erro deve ser clara quando o valor for invalido.
- Testes devem cobrir entrada com virgula e com ponto.
Após testes e prints
Foram analisadas telas reais do sistema durante o uso da funcionalidade de cadastro de estrutura, status dos bancos, validacao de leg, listagem de estruturas e execucao do pipeline.
Evidencias observadas
1. Erro de validacao numerica confirmado
Foi observado erro em tela:
  		strike must be numeric
O erro ocorre ao informar valor com virgula decimal, por exemplo:
    		158,00
Porem, apos estrutura salva ou exibida nos detalhes, o sistema apresenta os valores ja normalizados com ponto decimal, por exemplo:
    		Strike: 158.0    Premio: 1.51
Conclusao:
- A falha esta provavelmente na validacao inicial do formulario ou no comando de aplicar/salvar leg.- O dominio ou a exibicao posterior ja consegue trabalhar com valor numerico convertido.- A correcao deve ocorrer antes da validacao "must be numeric", normalizando virgula para ponto quando aplicavel.
Ajuste no criterio de aceite:
- O botao "Aplicar Leg" deve aceitar strike e premio com virgula decimal.- O botao "Salvar" deve aceitar legs com valores digitados em formato brasileiro.- A mensagem "strike must be numeric" nao deve aparecer para valores validos como 158,00.

2. Definição refinada da inclusão assistida por dados automáticos

A inclusao de estruturas deve seguir um modelo em que o usuario informe apenas os campos principais da operacao, e os demais campos sejam preenchidos automaticamente a partir do simbolo da opcao.
Campos obrigatorios informados pelo usuario:
Dados da estrutura
Nome da estrutura.
Dados de cada leg
- Lado: compra ou venda.- Tipo: put ou call.- Quantidade executada.- Valor executado, equivalente ao premio/preco da operacao.- Simbolo da opcao.
Campos que devem ser preenchidos automaticamente apos informar o simbolo da opcao:
- Ativo objeto.- Strike.- Vencimento.- Multiplicador, quando disponivel.- Demais metadados da opcao necessarios para calculo, payoff e decisoes.
Observacao importante:
Mesmo que o simbolo da opcao permita inferir tipo, vencimento ou strike, o sistema deve validar a consistencia entre:
- simbolo informado;- tipo informado pelo usuario;- dados retornados automaticamente.
Exemplo:
Se o usuario informar tipo CALL, mas o simbolo identificado pelo cadastro/RTD/base local for PUT, o sistema deve alertar a divergencia antes de salvar.
Criterios de aceite complementares:
- Ao digitar ou aplicar o simbolo da opcao, o sistema deve buscar automaticamente os dados da opcao.- O usuario nao deve precisar digitar manualmente strike e vencimento quando o simbolo for reconhecido.- Se o simbolo nao for encontrado, o sistema deve informar claramente.- Se houver divergencia entre simbolo, tipo e ativo, o sistema deve bloquear ou pedir confirmacao.- A estrutura so deve ser salva como funcional se possuir dados minimos para payoff e decisoes.

3. Estrutura incluída aparece no sistema, mas curva de payoff não funciona e busca de decisões também não.

Após testes e prints
Foi observado que a estrutura cadastrada aparece na aba "Estruturas", com ID e legs preenchidas.
Exemplo observado:
- ID: 2- Nome: SBSP+SMAL=BOVA- Ativo: BOVA11- Status: active- Quantidade de legs: 4
A tela de detalhes mostra as legs corretamente:
- Leg 1: comprado call- Leg 2: vendido call- Leg 3: vendido put- Leg 4: comprado put
Porem, a tela de status dos bancos informa:
    	Consolidacao: structure_decisions (linhas: 0, estruturas: 0)
Impacto
O cadastro da estrutura fica apenas visual, mas nao funcional. Isso quebra o fluxo principal do sistema. Curva de payoff nao e gerada, busca de decisões nao retorna ou nao executa corretamente.
Conclusao:
A estrutura existe na tabela/listagem de estruturas, mas nao foi consolidada para a tabela ou visao usada pelo motor de decisoes.
Hipoteses iniciais
Possiveis causas:
- Estrutura esta sendo salva sem legs completas.
- Legs estao sem campos obrigatorios para calculo.
- Quantidade, preco, strike ou tipo da opcao estao nulos ou invalidos.
- Normalizacao de comprado e vendido nao esta sendo aplicada no cadastro manual.
- Servico de payoff espera campos que nao sao preenchidos na inclusao.
- Motor de decisoes nao esta recebendo a estrutura recem-cadastrada.
- Falta recalculo apos salvar a estrutura.
- Estrutura aparece na tela, mas nao foi persistida no formato esperado pelos servicos.
Hipoteses refinadas:
- O pipeline nao esta processando estruturas cadastradas manualmente.- A estrutura nova nao atende algum filtro de consolidacao.- O status "active" nao esta sendo considerado corretamente.- O campo structure_id pode nao estar sendo gravado ou relacionado corretamente.- O modo canonical pode estar filtrando a estrutura incorretamente.- A consolidacao ignora estruturas criadas pela interface manual.- Faltam campos derivados exigidos por structure_decisions.- A estrutura tem legs suficientes para exibicao, mas nao suficientes para decisao.
Tarefas complementares:
- Verificar se a estrutura ID 2 existe na tabela principal de estruturas.- Verificar se as 4 legs existem na tabela de legs.- Verificar se o pipeline le essa estrutura.- Verificar por que structure_decisions permanece com 0 linhas.- Registrar quais estruturas foram lidas, ignoradas ou rejeitadas pelo pipeline.- Criar log de motivo quando uma estrutura for ignorada pela consolidacao.
Criterio de aceite
- Criar estrutura manual com uma ou mais legs validas.
- Abrir a estrutura cadastrada.
- Gerar curva de payoff sem erro.
- Executar busca de decisoes usando a estrutura.
- Exibir mensagem clara se faltar dado obrigatorio.
- Adicionar ou ajustar testes cobrindo esse fluxo.
Criterio de aceite complementar:
Apos cadastrar uma estrutura manual ativa e executar o pipeline, a tabela structure_decisions deve conter registros vinculados a essa estrutura, ou o sistema deve informar claramente por que ela foi rejeitada.
Pontos a revisar
- Fluxo de salvamento da estrutura.
- Entidade ou modelo de estrutura.
-	 Entidade ou modelo de leg.
- Servico de payoff.
- Servico de busca de decisoes.
- Mapeamento entre dados da interface e dados do dominio.
- Logs de erro silencioso.
- Testes existentes de payoff e decisoes.
Correcao esperada
Apos incluir uma estrutura valida:
- A estrutura deve aparecer na listagem.
- A estrutura deve possuir legs validas.
- A curva de payoff deve ser calculada.
- A busca de decisoes deve conseguir usar a estrutura.
- Em caso de dados insuficientes, o sistema deve informar o motivo.

4. Botão atualizar dados nao apresenta feedback e aparentemente nao executa acão

Sintoma
Ao clicar em atualizar dados:
- Nada visivel acontece.
- Nao aparece mensagem de sucesso.
- Nao aparece mensagem de erro.
- Os dados nao mudam.
- O usuario nao sabe se houve execucao.
Impacto
O usuario perde confianca no sistema e nao consegue saber se a atualizacao foi executada, falhou ou esta em andamento.
Hipoteses iniciais
Possiveis causas:
- O botao nao esta conectado a uma acao real.
- A acao executa, mas nao atualiza a tela.
- A acao falha silenciosamente.
- Excecoes estao sendo capturadas sem exibicao.
- Nao ha loading, toast, alerta ou log visivel.
- O servico de atualizacao nao retorna status.

Pontos a revisar
- Handler do botao atualizar dados.
- Servico chamado pelo botao.
- Tratamento de sucesso.
- Tratamento de erro.
- Atualizacao do estado da tela.
- Logs de execucao.
- Mensagens para o usuario.
Correcao esperada
Ao clicar em atualizar dados, o sistema deve:
1. Mostrar que iniciou a atualizacao.
2. Executar a rotina correspondente.
3. Informar sucesso ou erro.
4. Atualizar os dados exibidos quando aplicavel.
5. Registrar detalhes tecnicos em log.
Criterios de aceite
- Clique no botao gera algum feedback imediato.
- Sucesso exibe mensagem clara.
- Erro exibe mensagem clara.
- Erro tecnico fica registrado em log.
- Dados exibidos sao atualizados quando a rotina conclui com sucesso.
Payoff provavelmente nao esta sendo gerado para estrutura manual	
	Foi observado no status dos bancos:
Tabela de payoff: payoff_curve_points    Filtro de estrutura ativo: structure_id (mode=canonical)
Porem a curva de payoff nao funciona para a estrutura cadastrada manualmente.
Conclusão:
A tabela de pontos de payoff existe, mas a estrutura manual provavelmente nao possui pontos gerados ou nao esta sendo localizada pelo filtro ativo.
Hipoteses refinadas:
- payoff_curve_points nao recebe dados para estruturas manuais.- O gerador de payoff depende da consolidacao em structure_decisions.- O filtro por structure_id em modo canonical nao encontra a estrutura criada manualmente.- O pipeline nao chama a etapa de payoff para estruturas novas.- Existem dados suficientes para exibir as legs, mas nao para gerar curva.
Tarefas complementares:
- Verificar se existem registros em payoff_curve_points para a estrutura ID 2.- Verificar se o payoff usa o mesmo ID exibido na tela de estruturas.- Verificar se o modo canonical transforma ou troca o identificador da estrutura.- Adicionar mensagem quando nao houver pontos de payoff gerados.- Adicionar log com total de pontos de payoff criados por estrutura.
Criterio de aceite complementar:
- Ao salvar estrutura manual valida e executar pipeline, devem ser gerados pontos em payoff_curve_points para a estrutura.- Se os pontos nao forem gerados, o sistema deve informar o motivo.

5. Atualizacoes RTD nao executadas mesmo com conexao aberta

Sintoma
Mesmo com conexao RTD aberta, as atualizacoes RTD nao foram executadas ou nao refletiram no sistema.
Impacto
Dados de mercado podem ficar desatualizados, afetando precificacao, payoff, decisoes e confiabilidade da estrutura.
Hipoteses iniciais

Possiveis causas:
- O sistema detecta a conexao aberta, mas nao dispara a coleta.
- A rotina RTD nao esta sendo chamada pelo botao atualizar dados.
- A coleta RTD executa, mas nao persiste no banco.
- A coleta persiste, mas a tela nao recarrega os dados.
- Ha erro silencioso no adaptador RTD.
- Tickers ou simbolos enviados ao RTD estao incorretos.
- A tabela rtd_option_quotes nao esta sendo atualizada.
- O fluxo usa cache antigo.
- O status de conexao RTD nao representa execucao real de coleta.
Pontos a revisar
- Adaptador RTD.
- Servico de atualizacao RTD.
- Integracao entre botao atualizar dados e RTD.
- Persistencia em rtd_option_quotes.
- Logs da rotina RTD.
- Atualizacao da tela apos coleta.
- Tratamento de erro quando o RTD nao retorna dados.
- Normalizacao de tickers usados na consulta.
Correcao esperada
Com conexao RTD aberta:
- O sistema deve conseguir disparar atualizacao RTD.
- O sistema deve registrar se a coleta foi executada.
- O sistema deve informar quantos registros foram atualizados.
- A tabela ou repositorio de cotacoes RTD deve receber os dados.
- A interface deve refletir os dados atualizados.
- Falhas devem gerar mensagem clara.
Criterios de aceite
- Com RTD conectado, atualizar dados executa coleta.
- Sistema informa sucesso ou falha.
- Dados RTD sao persistidos ou atualizados.
- Tela mostra dados novos ou horario da ultima atualizacao.
- Logs permitem diagnosticar falhas.
Ordem proposta de execucao
Fase 1. Reproducao controlada dos problemas
Objetivo:
Confirmar cada problema em ambiente local e registrar o comportamento atual.
Tarefas:
1. Criar uma estrutura manual usando ponto decimal.
2. Criar uma estrutura manual usando virgula decimal.
3. Verificar se a estrutura salva gera payoff.
4. Verificar se a estrutura salva participa da busca de decisoes.
5. Clicar em atualizar dados e observar logs, tela e banco.
6. Testar atualizacao RTD com conexao aberta.
7. Registrar prints, logs ou saidas relevantes.
Saida esperada:
- Lista dos problemas confirmados.
- Lista dos problemas nao reproduzidos.
- Logs relevantes.
- Estado do banco antes e depois dos testes.
Revisao do problema "Atualizar dados"
A analise anterior indicava que ao clicar em atualizar dados nada acontecia. Com os novos prints, foi observado que em alguns casos o sistema exibe mensagem:
Pipeline executado com sucesso!
Portanto, o problema deve ser refinado.
Problema atualizado:
	O sistema pode exibir mensagem de sucesso do pipeline, mas essa mensagem e generica e nao comprova que as etapas esperadas foram realmente executadas ou que produziram resultado.
O feedback atual nao informa:
- quantas estruturas foram processadas;- quantas estruturas foram ignoradas;- quantas decisoes foram geradas;- quantos pontos de payoff foram criados;- se houve atualizacao RTD;- quantas cotacoes RTD foram atualizadas;- se alguma etapa falhou parcialmente.
Criterios de aceite atualizados:
Ao executar o pipeline ou atualizar dados, o sistema deve exibir resumo semelhante a:
Pipeline concluido.    Estruturas lidas: X    Estruturas processadas: Y    Estruturas ignoradas: Z    Decisoes geradas: N    Pontos de payoff gerados: M    Cotacoes RTD atualizadas: R    Avisos: A    Erros: E
Se tudo retornar zero, o sistema nao deve apenas mostrar "sucesso". Deve informar:
Pipeline executado, mas nenhum dado novo foi gerado.

6. Possivel divergencia de horário

Na tela de detalhes da estrutura foi observado campo "Atualizado" com horario aparentemente posterior ao horario local do teste.
Ponto a verificar:
- Confirmar se os timestamps estao sendo gravados em UTC, horario local ou sem timezone.- Padronizar exibicao para America/Sao_Paulo ou indicar explicitamente UTC.
Criterio de aceite:
- Campos "Criado em" e "Atualizado em" devem ser consistentes e compreensiveis para o usuario.


TAREFAS DAS FASES

Fase 2. Correcao da normalizacao numerica
Objetivo:
Permitir entrada de valores numericos no formato brasileiro e no formato tecnico.
Tarefas:
1. Identificar pontos de conversao de strike, preco e quantidade.
2. Criar ou ajustar funcao central de normalizacao numerica.
3. Aplicar a normalizacao antes da validacao.
4. Ajustar mensagens de erro.
5. Criar testes unitarios.
6. Criar teste do fluxo de inclusao manual.

Saida esperada:
- Cadastro aceita virgula decimal.
- Cadastro aceita ponto decimal.
- Testes cobrindo ambos os formatos.

Fase 3. Revisao do cadastro de estrutura e integracao com payoff
Objetivo:
Garantir que a estrutura cadastrada manualmente fique pronta para uso funcional.
Tarefas:
1. Mapear campos obrigatorios para payoff.
2. Mapear campos obrigatorios para busca de decisoes.
3. Comparar estrutura criada manualmente com estrutura usada nos testes existentes.
4. Corrigir mapeamento de legs.
5. Garantir normalizacao de comprado e vendido.
6. Garantir preenchimento de strike, tipo, quantidade, preco e vencimento quando necessarios.
7. Adicionar validacao antes de salvar.
8. Exibir mensagem se a estrutura estiver incompleta.
9. Criar teste integrado de cadastro manual ate payoff.
10. Criar teste integrado de cadastro manual ate busca de decisoes.
Saida esperada:
- Estrutura cadastrada gera payoff.
- Estrutura cadastrada participa da busca de decisoes.
- Falhas por dados incompletos sao explicadas ao usuario.

Fase 4. Revisao do botao atualizar dados
Objetivo:
Garantir que o botao tenha acao rastreavel, feedback visual e tratamento de erro.
Tarefas:
1. Identificar handler do botao.
2. Confirmar qual servico deve ser chamado.
3. Adicionar feedback de inicio.
4. Adicionar feedback de sucesso.
5. Adicionar feedback de erro.
6. Registrar logs tecnicos.
7. Atualizar a tela apos sucesso.
8. Criar teste ou verificacao manual documentada.
Saida esperada:
- Botao nao fica mais silencioso.
- Usuario sabe se a atualizacao iniciou, concluiu ou falhou.
- Logs ajudam no diagnostico.

Fase 5. Revisao da execucao RTD
Objetivo:
Garantir que a conexao RTD aberta resulte em atualizacao efetiva dos dados.
Tarefas:
1. Verificar como o sistema detecta conexao RTD.
2. Verificar como a rotina RTD e disparada.
3. Verificar se o botao atualizar dados chama a rotina RTD.
4. Verificar se os dados retornados sao persistidos.
5. Verificar se rtd_option_quotes e atualizada.
6. Verificar se a tela usa os dados novos.
7. Adicionar contagem de registros atualizados.
8. Adicionar mensagem de erro quando nenhum dado for retornado.
9. Criar teste com mock ou simulacao de RTD.
10. Documentar limitacoes quando depender de ambiente externo.
Saida esperada:
- Atualizacao RTD executa quando solicitada.
- Sistema informa resultado da coleta.
- Dados atualizados ficam disponiveis para pricing, payoff e decisoes.

Fase 6. Validacao integrada
Objetivo:
Confirmar que as correcoes nao quebraram funcionalidades existentes.
Tarefas:
1. Executar testes completos.
2. Executar compileall.
3. Testar fluxo manual de cadastro.
4. Testar fluxo automatico ou assistido, se implementado.
5. Testar payoff.
6. Testar busca de decisoes.
7. Testar atualizacao de dados.
8. Testar RTD com conexao aberta.
9. Registrar evidencia final.
Comandos previstos:
python -m pytest ATT/tests -q
 	python -m compileall repositories services domain ATT/tests
Saida esperada:
- Testes aprovados.
- Compilacao sem erro.
- Fluxos principais validados.
- Evidencia documental criada.
Checklist de correcao

| Item | Situacao inicial | Situacao esperada | Status |
|---|---|---|---|
| Aceitar virgula em strike | Falha | Aceita virgula e ponto | Pendente |
| Aceitar virgula em precos | A verificar | Aceita virgula e ponto | Pendente |
| Cadastro manual funcional | Parcial | Estrutura pronta para payoff e decisoes | Pendente |
| Payoff apos cadastro | Falha | Curva gerada | Pendente |
| Busca de decisoes apos cadastro | Falha | Busca executada | Pendente |
|Botao atualizar dados | Feedback inexistente ou genérico | Feedback detalhado e execução rastreável | Pendente
| Atualizacao RTD | Nao executada | Coleta executada e registrada | Pendente |
| Logs de erro | Insuficientes | Logs claros | Pendente |
| Testes automatizados | A ajustar | Cobertura dos fluxos corrigidos | Pendente |
| Evidencia final | Inexistente | Documento de fechamento da revisao | Pendente |

Riscos
1. Dependencia de ambiente externo RTD.
2. Diferenca entre dados manuais e dados automaticos.
3. Erros silenciosos ja existentes dificultarem diagnostico.
4. Validacoes muito permissivas aceitarem dados incorretos.
5. Alteracao no cadastro afetar testes existentes.
Decisoes preliminares
1. Nao iniciar novas funcionalidades antes de corrigir os fluxos quebrados.
2. Priorizar primeiro o cadastro manual funcional.
3. Em seguida corrigir payoff e busca de decisoes.
4. Depois corrigir feedback do botao atualizar dados.
5. Por fim estabilizar RTD e fluxo automatico.
6. Toda correcao deve ter teste ou evidencia manual registrada.

Resultado esperado da rota
Ao final desta revisao, o sistema deve permitir:
1. Cadastrar estrutura manualmente com numeros no formato brasileiro.
2. Usar a estrutura cadastrada para gerar payoff.
3. Usar a estrutura cadastrada na busca de decisoes.
4. Atualizar dados com feedback claro ao usuario.
5. Executar atualizacao RTD quando houver conexao disponivel.
6. Validar tudo com testes e evidencia documental.
