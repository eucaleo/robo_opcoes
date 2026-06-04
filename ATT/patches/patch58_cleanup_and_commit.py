# patch58_cleanup_and_commit.py
"""
patch_58: housekeeping pós-patch_57
  1. Remove todos os .bak_emoji (untracked)
  2. Remove fix_patch57[d-j].py da raiz
  3. Remove add_patch57_to_audit.py, fix_count_occurrences_bug.py, fix_headers_final.py
  4. Remove scripts/tmp_audit_structure_ref_candidates.py
  5. Remove ATT/patches/backups/ (backups temporários do patch_56)
  6. git rm dos tracked deletions
  7. git add -u de todos os modified
  8. Commit único patch_58
"""
import pathlib, subprocess, sys, shutil

ROOT = pathlib.Path(__file__).parent.resolve()

# ── 1. Deleções por glob ──────────────────────────────────────────────────────

DELETE_PATTERNS = [
    "**/*.bak_emoji",
]

# ── 2. Deleções exatas (relativos à ROOT) ─────────────────────────────────────

DELETE_EXACT = [
    # iterativos patch_57 na raiz
    "fix_patch57d.py",
    "fix_patch57e.py",
    "fix_patch57f.py",
    "fix_patch57g.py",
    "fix_patch57h.py",
    "fix_patch57i.py",
    "fix_patch57j.py",
    # outros resíduos na raiz
    "add_patch57_to_audit.py",
    "fix_count_occurrences_bug.py",
    "fix_headers_final.py",
    # temporário esquecido em scripts/
    "scripts/tmp_audit_structure_ref_candidates.py",
    # shell script avulso
    "ATT/patches/apply_patch_56.sh",
]

# ── 3. Diretórios a remover ───────────────────────────────────────────────────

DELETE_DIRS = [
    "ATT/patches/backups",       # ← caminho correto confirmado
]

# ── 4. Tracked deletions (git rm --cached) ────────────────────────────────────

TRACKED_DELETIONS = [
    "UI/models/ui_data.py.bak_p38_20260603_093827",
    "ATT/patches/backups/patch_56/derived_repo_20260603_205947.py",
    "ATT/patches/backups/patch_56/derived_service_20260603_205947.py",
    "scripts/tmp_fix_todos_patch53b.py",
    "scripts/tmp_show_todos_patch53.py",
    "scripts/tmp_verify_patch53b.py",
]

# ─────────────────────────────────────────────────────────────────────────────

removed, skipped = [], []

print("\n── LIMPEZA DE ARQUIVOS ──────────────────────────────────────────────")

for pattern in DELETE_PATTERNS:
    for f in sorted(ROOT.glob(pattern)):
        try:
            f.unlink()
            removed.append(str(f.relative_to(ROOT)))
        except Exception as e:
            skipped.append((str(f.relative_to(ROOT)), str(e)))

for rel in DELETE_EXACT:
    p = ROOT / rel
    if p.exists():
        p.unlink()
        removed.append(rel)
    else:
        skipped.append((rel, "não encontrado"))

for rel in DELETE_DIRS:
    p = ROOT / rel
    if p.exists() and p.is_dir():
        shutil.rmtree(p)
        removed.append(rel + "/")
    else:
        skipped.append((rel + "/", "não encontrado"))

for r in removed:
    print(f"  DEL  {r}")
for s, reason in skipped:
    print(f"  SKIP {s}  ({reason})")

print(f"\n  Removidos : {len(removed)}")
print(f"  Skipped   : {len(skipped)}")

# ── git rm tracked ────────────────────────────────────────────────────────────

print("\n── GIT RM (tracked deletions) ───────────────────────────────────────")

for rel in TRACKED_DELETIONS:
    r = subprocess.run(
        ["git", "rm", "--cached", "--ignore-unmatch", "-f", rel],
        capture_output=True, text=True, cwd=ROOT
    )
    out = r.stdout.strip() or r.stderr.strip() or "ok"
    status = "OK " if r.returncode == 0 else "ERR"
    print(f"  {status}  {rel}  |  {out}")

# ── git add -u ────────────────────────────────────────────────────────────────

print("\n── GIT ADD ──────────────────────────────────────────────────────────")

r = subprocess.run(["git", "add", "-u"], capture_output=True, text=True, cwd=ROOT)
if r.returncode == 0:
    print("  OK   git add -u")
else:
    print("  ERR ", r.stderr.strip())
    sys.exit(1)

# Conta staged
r = subprocess.run(
    ["git", "diff", "--cached", "--name-only"],
    capture_output=True, text=True, cwd=ROOT
)
staged = r.stdout.strip().splitlines()
print(f"  {len(staged)} arquivo(s) staged")

# ── git commit ────────────────────────────────────────────────────────────────

print("\n── GIT COMMIT ───────────────────────────────────────────────────────")

MSG = (
    "patch_58: housekeeping -- remove .bak_emoji, fix_patch57[d-j].py, "
    "tmp scripts, ATT/patches/backups/; "
    "sanitizacao emoji em ~100 arquivos commitada"
)

r = subprocess.run(
    ["git", "commit", "-m", MSG],
    capture_output=True, text=True, cwd=ROOT
)

if r.returncode == 0:
    h = subprocess.run(
        ["git", "log", "--oneline", "-1"],
        capture_output=True, text=True, cwd=ROOT
    )
    print(f"  OK   {h.stdout.strip()}")
elif "nothing to commit" in r.stdout + r.stderr:
    print("  SKIP nada para commitar")
else:
    print("  ERR ", r.stderr.strip())
    print(r.stdout)
    sys.exit(1)

# ── status final ─────────────────────────────────────────────────────────────

print("\n── STATUS FINAL ─────────────────────────────────────────────────────")

r = subprocess.run(
    ["git", "status", "--short"],
    capture_output=True, text=True, cwd=ROOT
)
remaining = r.stdout.strip()

if remaining:
    lines = remaining.splitlines()
    print(f"  {len(lines)} arquivo(s) ainda fora do commit:")
    for line in lines:
        print(f"    {line}")
else:
    print("  Working tree limpo ✅")

# log final
r = subprocess.run(
    ["git", "log", "--oneline", "-5"],
    capture_output=True, text=True, cwd=ROOT
)
print("\n  Últimos commits:")
for line in r.stdout.strip().splitlines():
    print(f"    {line}")

print("\n  ✅  patch_58 concluído.")
