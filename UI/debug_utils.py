"""
debug_utils.py - Controle centralizado de logs da UI

Env vars:
- UI_DEBUG=1    : debug detalhado
- UI_DEBUG=0    : silencioso (default)
"""

import os

def is_debug():
    """Lê UI_DEBUG dinamicamente (não congela no import)"""
    return os.environ.get("UI_DEBUG", "0").strip() in ("1", "true", "True", "on")

def debug(*args, **kwargs):
    """Log apenas se UI_DEBUG=1"""
    if is_debug():
        print("[UI][DEBUG]", *args, **kwargs)

def info(*args, **kwargs):
    """Log sempre (info level)"""
    print("[UI]", *args, **kwargs)

def payoff_debug(*args, **kwargs):
    """Log de payoff chart apenas se debug ativo"""
    if is_debug():
        print("[PayoffChart] DEBUG", *args, **kwargs)

def payoff_info(*args, **kwargs):
    """Log de payoff sempre"""
    print("[PayoffChart]", *args, **kwargs)
