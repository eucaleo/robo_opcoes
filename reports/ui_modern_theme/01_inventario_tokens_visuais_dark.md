# Inventário de tokens visuais da UI moderna

Data de referência: 2026-07-02

Objetivo:

- localizar cores, estilos, dimensões e parâmetros visuais hardcoded no modo dark;
- preparar substituição futura por tokens centralizados em UI/modern/theme.py;
- não alterar código nesta etapa;
- não alterar layout funcional, banco ou regra de negócio.

## Arquivos analisados

- UI/modern/dark_window.py
- UI/modern/theme.py

## Resumo

- Ocorrências encontradas: 30

| Arquivo | Linha | Categoria | Trecho |
|---|---:|---|---|
| UI/modern/dark_window.py | 31 | appearance_theme | ctk.set_appearance_mode("Dark") |
| UI/modern/dark_window.py | 32 | appearance_theme | ctk.set_default_color_theme("blue") |
| UI/modern/theme.py | 20 | hex_color | "bg": "#020617", |
| UI/modern/theme.py | 21 | hex_color | "surface": "#0F172A", |
| UI/modern/theme.py | 22 | hex_color | "surface_alt": "#111827", |
| UI/modern/theme.py | 23 | hex_color | "card": "#111827", |
| UI/modern/theme.py | 24 | hex_color | "border": "#1F2937", |
| UI/modern/theme.py | 25 | hex_color | "text": "#F9FAFB", |
| UI/modern/theme.py | 26 | hex_color | "text_muted": "#9CA3AF", |
| UI/modern/theme.py | 27 | hex_color | "text_soft": "#CBD5E1", |
| UI/modern/theme.py | 28 | hex_color | "primary": "#2563EB", |
| UI/modern/theme.py | 29 | hex_color | "primary_hover": "#1D4ED8", |
| UI/modern/theme.py | 30 | hex_color | "success": "#22C55E", |
| UI/modern/theme.py | 31 | hex_color | "warning": "#F59E0B", |
| UI/modern/theme.py | 32 | hex_color | "danger": "#EF4444", |
| UI/modern/theme.py | 33 | hex_color | "info": "#38BDF8", |
| UI/modern/theme.py | 37 | hex_color | "bg": "#F3F4F6", |
| UI/modern/theme.py | 38 | hex_color | "surface": "#FFFFFF", |
| UI/modern/theme.py | 39 | hex_color | "surface_alt": "#F9FAFB", |
| UI/modern/theme.py | 40 | hex_color | "card": "#FFFFFF", |
| UI/modern/theme.py | 41 | hex_color | "border": "#E5E7EB", |
| UI/modern/theme.py | 42 | hex_color | "text": "#111827", |
| UI/modern/theme.py | 43 | hex_color | "text_muted": "#6B7280", |
| UI/modern/theme.py | 44 | hex_color | "text_soft": "#374151", |
| UI/modern/theme.py | 45 | hex_color | "primary": "#2563EB", |
| UI/modern/theme.py | 46 | hex_color | "primary_hover": "#1D4ED8", |
| UI/modern/theme.py | 47 | hex_color | "success": "#16A34A", |
| UI/modern/theme.py | 48 | hex_color | "warning": "#D97706", |
| UI/modern/theme.py | 49 | hex_color | "danger": "#DC2626", |
| UI/modern/theme.py | 50 | hex_color | "info": "#0284C7", |

## Diretriz para o próximo patch

- Substituir apenas tokens visuais por referências ao tema central.
- Não alterar callbacks.
- Não alterar consultas de banco.
- Não alterar services, controllers ou repositories.
- Não alterar layout funcional.
- Não alterar textos operacionais.
- Validar com py_compile, diagnóstico e abertura manual da UI moderna.

# Detalhamento

## UI/modern/dark_window.py

### Linha 31

Categorias: appearance_theme

Trecho:

    ctk.set_appearance_mode("Dark")

### Linha 32

Categorias: appearance_theme

Trecho:

    ctk.set_default_color_theme("blue")

## UI/modern/theme.py

### Linha 20

Categorias: hex_color

Trecho:

    "bg": "#020617",

### Linha 21

Categorias: hex_color

Trecho:

    "surface": "#0F172A",

### Linha 22

Categorias: hex_color

Trecho:

    "surface_alt": "#111827",

### Linha 23

Categorias: hex_color

Trecho:

    "card": "#111827",

### Linha 24

Categorias: hex_color

Trecho:

    "border": "#1F2937",

### Linha 25

Categorias: hex_color

Trecho:

    "text": "#F9FAFB",

### Linha 26

Categorias: hex_color

Trecho:

    "text_muted": "#9CA3AF",

### Linha 27

Categorias: hex_color

Trecho:

    "text_soft": "#CBD5E1",

### Linha 28

Categorias: hex_color

Trecho:

    "primary": "#2563EB",

### Linha 29

Categorias: hex_color

Trecho:

    "primary_hover": "#1D4ED8",

### Linha 30

Categorias: hex_color

Trecho:

    "success": "#22C55E",

### Linha 31

Categorias: hex_color

Trecho:

    "warning": "#F59E0B",

### Linha 32

Categorias: hex_color

Trecho:

    "danger": "#EF4444",

### Linha 33

Categorias: hex_color

Trecho:

    "info": "#38BDF8",

### Linha 37

Categorias: hex_color

Trecho:

    "bg": "#F3F4F6",

### Linha 38

Categorias: hex_color

Trecho:

    "surface": "#FFFFFF",

### Linha 39

Categorias: hex_color

Trecho:

    "surface_alt": "#F9FAFB",

### Linha 40

Categorias: hex_color

Trecho:

    "card": "#FFFFFF",

### Linha 41

Categorias: hex_color

Trecho:

    "border": "#E5E7EB",

### Linha 42

Categorias: hex_color

Trecho:

    "text": "#111827",

### Linha 43

Categorias: hex_color

Trecho:

    "text_muted": "#6B7280",

### Linha 44

Categorias: hex_color

Trecho:

    "text_soft": "#374151",

### Linha 45

Categorias: hex_color

Trecho:

    "primary": "#2563EB",

### Linha 46

Categorias: hex_color

Trecho:

    "primary_hover": "#1D4ED8",

### Linha 47

Categorias: hex_color

Trecho:

    "success": "#16A34A",

### Linha 48

Categorias: hex_color

Trecho:

    "warning": "#D97706",

### Linha 49

Categorias: hex_color

Trecho:

    "danger": "#DC2626",

### Linha 50

Categorias: hex_color

Trecho:

    "info": "#0284C7",

