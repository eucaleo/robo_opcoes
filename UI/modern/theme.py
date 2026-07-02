"""
Tokens de tema para a UI moderna.

Este módulo ainda não altera automaticamente os painéis existentes.
Ele prepara a convergência futura para um modelo único com temas
Dark/Clean sem duplicar janelas e componentes.
"""

from __future__ import annotations

from typing import Dict, Literal



# CustomTkinter runtime theme
CUSTOMTKINTER_APPEARANCE_MODE = "Dark"
CUSTOMTKINTER_COLOR_THEME = "blue"

ThemeName = Literal["dark", "clean"]


THEMES: Dict[str, Dict[str, str]] = {
    "dark": {
        "appearance_mode": "dark",
        "bg": "#020617",
        "surface": "#0F172A",
        "surface_alt": "#111827",
        "card": "#111827",
        "border": "#1F2937",
        "text": "#F9FAFB",
        "text_muted": "#9CA3AF",
        "text_soft": "#CBD5E1",
        "primary": "#2563EB",
        "primary_hover": "#1D4ED8",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "info": "#38BDF8",
    },
    "clean": {
        "appearance_mode": "light",
        "bg": "#F3F4F6",
        "surface": "#FFFFFF",
        "surface_alt": "#F9FAFB",
        "card": "#FFFFFF",
        "border": "#E5E7EB",
        "text": "#111827",
        "text_muted": "#6B7280",
        "text_soft": "#374151",
        "primary": "#2563EB",
        "primary_hover": "#1D4ED8",
        "success": "#16A34A",
        "warning": "#D97706",
        "danger": "#DC2626",
        "info": "#0284C7",
    },
}


def get_theme(name: str = "dark") -> Dict[str, str]:
    """
    Retorna os tokens de tema.

    Parameters
    ----------
    name:
        Nome do tema. Valores aceitos: "dark" ou "clean".
    """
    normalized = (name or "dark").strip().lower()

    if normalized not in THEMES:
        available = ", ".join(sorted(THEMES))
        raise ValueError(f"Tema inválido: {name!r}. Temas disponíveis: {available}")

    return THEMES[normalized].copy()
