# Limpeza e encerramento da frente

## Objetivo

Evitar que a frente deixe arquivos temporários, código morto ou documentação duplicada.

## Ao encerrar cada fase

Verificar:

- Arquivos criados.
- Arquivos alterados.
- Scripts temporários.
- Relatórios de auditoria.
- Testes adicionados.
- Código antigo removido.

## Ao encerrar a frente inteira

Classificar a pasta `FRENTE_RTD_EXCEL_BTG_ONLINE/`:

### Manter

Documentação final que explica a arquitetura implementada.

### Mover

Documentos que devem ir para `ATT/patches`, `docs` ou local definitivo do projeto.

### Remover

Relatórios temporários e arquivos de auditoria que não precisam permanecer.

## Checklist final

- Git limpo.
- Testes acumulativos passando.
- Banco íntegro.
- Código morto removido.
- Scripts antigos sob demanda removidos ou marcados como manutenção emergencial.
- Documentação final atualizada.
