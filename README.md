![alt text](https://www.ideis.pl/krakow/sites/ideis_krakow/files/styles/width_768/public/oembed_thumbnails/2026-03/FwpqzJ_BKR8RqA1RBNJ7IPFH6Esq8ABeXZXvZ4T_x2Y.jpg.webp?itok=5fN2oIZg)

# Release Notes Generator

Narzędzie do automatycznego generowania release notes z commitów Git z wykorzystaniem LLM.

## Zespół
- Michał 55335 - Project Manager / Lead Developer
- Adrian 52645 - DevOps Engineer
- Emilia 52766 - UX Engineer
- Krystian 52883 - QA Engineer

### Prowadzący:
mgr inż. Aleksandra Ata

## Wymagania

- Python 3.8+
- Klucz API OpenAI

## Instalacja

```bash
git clone https://github.com/ProXi-22/release_notes_generator
cd release_notes_generator
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

## Konfiguracja

Utwórz plik `.env` w głównym katalogu projektu:

```
OPENAI_API_KEY=<klucz_API>
```

## Uruchomienie

### Tryb CLI

```bash
python main.py --repo <url_lub_ścieżka_lokalna> --od <commit_start> --do <commit_end>
```

### Tryb GUI

```bash
python gui.py
```

### Parametry

| Parametr | Opis                                        | Przykład |
|----------|---------------------------------------------|---------|
| `--repo` | URL repozytorium GitHub lub ścieżka lokalna | `https://github.com/user/repo` lub `.` |
| `--od`   | Commit/tag początku zakresu                 | `HEAD~5`, `v1.0.0` |
| `--do`   | Commit/tag końca zakresu                    | `HEAD`, `v1.1.0` |

### Przykłady

Repozytorium zdalne (zostanie sklonowane tymczasowo):
```bash
python main.py --repo https://github.com/user/projekt --od HEAD~5 --do HEAD
```

Repozytorium lokalne (bieżący katalog):
```bash
python main.py --repo . --od HEAD~5 --do HEAD
```

### Wynik

Po uruchomieniu w konsoli pojawi się:
```
Klonowanie repozytorium z: https://github.com/user/projekt
Znaleziono 5 commitów.

Generowanie release notes...
Zapisano: release_notes_projekt_2026-06-13.md
```

W katalogu roboczym zostanie zapisany plik `release_notes_<nazwa-repo>_<data>.md` z treścią w formacie Markdown, np.:

```markdown
## Nowości
- Dodano obsługę argumentu --do w module CLI

## Poprawki błędów
- Naprawiono błąd przy klonowaniu repo z ukośnikiem na końcu URL

## Zmiany techniczne
- Wydzielono stałe konfiguracyjne do config.py
```

## Testy

```bash
python -m pytest testy.py -v
```

Pokrycie testami obejmuje moduł `modul_git.py` (3 testy jednostkowe).

## Technologie

- [GitPython](https://gitpython.readthedocs.io) — obsługa repozytoriów Git
- [OpenAI Python SDK](https://platform.openai.com/docs/libraries) — komunikacja z GPT-4o-mini
- [python-dotenv](https://pypi.org/project/python-dotenv/) — wczytywanie zmiennych środowiskowych
- [pytest](https://docs.pytest.org) — testy jednostkowe
- [tkinter](https://docs.python.org/3/library/tkinter.html) — interfejs graficzny
