# Fase 7 - Isolamento de Nomes Físicos Legados

## Objetivo

Isolar referências diretas a nomes físicos legados de tabelas `rtd_*` e `manual_*` fora das camadas autorizadas de acesso a dados.

A Fase 7 teve como foco reduzir vazamentos de vocabulário físico do banco em camadas de domínio, serviços e UI, mantendo esses nomes restritos às fronteiras apropriadas.

## Fronteiras permitidas

Após a Fase 7, referências a nomes físicos legados são consideradas permitidas apenas em:

- `repositories/**`
- `bridge_ingest_csv.py`
- `ATT/tests/**`
- `docs/**`

As seguintes camadas devem permanecer sem referências diretas a tabelas físicas legadas:

- `domain/**`
- `services/**`
- `UI/**`

## Alterações realizadas

### 1. Redução de referências físicas em domínio e facade

Commit:

- `997501d` - `Reduz referencias fisicas rtd em dominio e facade`

Arquivos tratados:

- `domain/market_snapshot.py`
- `services/canonical_pricing_facade.py`

Resumo:

- Removidas referências textuais/documentais diretas a `rtd_analise_robo`.
- Substituída linguagem física/legada por linguagem canônica/de mercado.
- Nenhuma regra de negócio foi alterada.

Validação executada:

```bash
git grep -n "rtd_analise\\|manual_analise" -- domain/market_snapshot.py services/canonical_pricing_facade.py || true

