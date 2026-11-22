# 002 — Pełna lista kolorów w tabeli puszek z magazynu

Status: zamknięta (czeka na publikację)  ·  Data: 2026-11-22

## 1. TL;DR
Tabela „Formats in our warehouse” dostaje wszystkie dostępne kolory wg listy od właściciela (panel Asaszi / Bagpak, 22.11.2026): 17 pozycji → 15 wierszy (500 ml silver i black matt z dwóch źródeł scalone). Potwierdzenie: tabela w EN/UA/ET ma 15 wierszy, test przechodzi.

## 2. Abstrakt
Tabela miała 10 wierszy: 200/250 slim tylko silver, 330 standard silver i „black” (bez „matt”), 500 z niejasnym kolorem „Black/white matt”. Zdjęcia w hero (spec 001) pokazują białe i czarne puszki, których tabela nie zawierała. Właściciel przesłał pełną listę dostępnych rozmiarów i kolorów. Dane paletowe (sztuk na warstwę, warstwy, wymiary) są cechą formatu, nie koloru — nowe kolory dziedziczą dane z istniejącego wiersza tego formatu. „Black/white matt” rozbite na osobne „Black matt” i „White matt”.

## 3. Cel
- **Cele:** wiersze: 200 slim silver/black matt; 250 slim silver/black matt; 330 sleek silver/black matt/white matt; 330 standard silver/black matt/white matt; 440 silver/black matt; 500 silver/black matt/white matt.
- **Poza zakresem:** zmiana zdjęć, wieczka, indeksy Bagpak.
- **Kryteria sukcesu:** 15 wierszy w każdym języku, nazwy kolorów przetłumaczone, brak „Black/white matt” i gołego „Black”.

## 4. Inwentarz artefaktów
- `src/en.html` — do zmiany: tablica `cans`, słownik `T`, mapa `chip`, klasa `.c-white`
- `build.py`, `lang_et.py` — do zmiany: słownik `T` w UA/ET
- `tests/check_site.py` — do zmiany: bramka liczby wierszy tabeli

## 5. Zmiany w domenie funkcjonalnej
Tabela renderowana w JS z tablicy `cans`; kolory jako „chip” z kółkiem. Biały chip z obwódką, żeby był widoczny na jasnym tle. Brak wpływu na SEO/przekierowania.

## 6. Ścieżka krytyczna
Tablica + słowniki → test → podgląd tabeli → zgoda → push.

## 7. Bramki kontrolne
| Bramka | Warunek | Weryfikacja | Blokuje |
|--------|---------|-------------|---------|
| Build/spójność | PASS | `python3 tests/check_site.py` | commit |
| Tabela | dokładnie 15 wierszy w `cans` | test | commit |
| **Negatywna** | brak `bwmatt` / „Black/white matt” | test | commit |
| Ręczna | tabela czytelna na telefonie i desktopie | podgląd | push |

## 8. Oczekiwany wynik
Klient widzi pełną ofertę kolorów; zdjęcia i tabela są spójne (poza 250 ml white — zob. pkt 9). Rollback: `git revert`.

## 9. Informacje dodatkowe
- Otwarte: zdjęcie 250 ml slim w hero pokazuje białą puszkę, której nie ma w ofercie (250 ml tylko silver i black matt).
- Dane palet: decyzja właściciela 22.11.2026 — wymiary wg tabeli na asaszi.pl (200 slim 1100 × 1200 × 2060; 250 slim 550/warstwę, 9 350/paletę; 500 ml 2174 mm). Kolejność wymiarów zostaje jak na stronie PW (krótszy bok pierwszy). Lid 330 sleek zostaje „200 / 202”.
- Indeksy Bagpak (np. SM/20-BLANK0002) nie są pokazywane na stronie — decyzja właściciela.
