from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ARQUIVOS = [
    ROOT / "services" / "terminal_vwap_payoff_app_service.py",
    ROOT / "controllers" / "terminal_vwap_payoff_controller.py",
    ROOT / "UI" / "components" / "terminal_vwap_payoff_dark_panel.py",
]


class CallAudit(ast.NodeVisitor):
    def __init__(self, arquivo: Path) -> None:
        self.arquivo = arquivo
        self.definicoes = []
        self.chamadas_com_structure_id = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name == "_call_first_available":
            argumentos = [arg.arg for arg in node.args.args]
            argumentos += [arg.arg for arg in node.args.kwonlyargs]
            if node.args.vararg:
                argumentos.append(f"*{node.args.vararg.arg}")
            if node.args.kwarg:
                argumentos.append(f"**{node.args.kwarg.arg}")

            self.definicoes.append(
                {
                    "linha": node.lineno,
                    "argumentos": argumentos,
                }
            )

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "_call_first_available"
        ):
            keywords = [kw.arg for kw in node.keywords if kw.arg is not None]

            if "structure_id" in keywords:
                self.chamadas_com_structure_id.append(
                    {
                        "linha": node.lineno,
                        "keywords": keywords,
                    }
                )

        self.generic_visit(node)


def main() -> int:
    encontrou_erro = False

    print("=" * 72)
    print("AUDITORIA: CONTRATO _call_first_available / structure_id")
    print("=" * 72)

    for arquivo in ARQUIVOS:
        print(f"\nArquivo: {arquivo.relative_to(ROOT)}")

        if not arquivo.exists():
            print("  [AVISO] Arquivo não encontrado.")
            continue

        try:
            arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            print(f"  [ERRO] Erro de sintaxe: linha {exc.lineno}: {exc.msg}")
            encontrou_erro = True
            continue

        auditoria = CallAudit(arquivo)
        auditoria.visit(arvore)

        for definicao in auditoria.definicoes:
            argumentos = ", ".join(definicao["argumentos"])
            print(
                f"  Definição encontrada na linha "
                f"{definicao['linha']}: ({argumentos})"
            )

        for chamada in auditoria.chamadas_com_structure_id:
            encontrou_erro = True
            keywords = ", ".join(chamada["keywords"])
            print(
                f"  [FALHA] Linha {chamada['linha']}: "
                f"_call_first_available recebe structure_id como keyword "
                f"({keywords})"
            )

    print("\n" + "=" * 72)
    if encontrou_erro:
        print("[FALHOU] Há incompatibilidade de contrato a corrigir.")
        return 1

    print("[OK] Nenhuma chamada incompatível foi encontrada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
