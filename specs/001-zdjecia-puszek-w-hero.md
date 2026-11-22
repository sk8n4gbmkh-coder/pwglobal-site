# 001 — Zdjęcia puszek w hero zamiast rysunku

Status: wdrożona 2026-11-22  ·  Data: 2026-11-22

## 1. TL;DR
W nagłówku strony (hero) rysunek SVG z sylwetkami 6 formatów puszek zastępujemy pokazem 3 zdjęć (250 ml slim, 330 ml standard, 500 ml standard), zmieniających się automatycznie. Cel: więcej dynamiki. Potwierdzenie: zdjęcia widoczne i przełączają się w EN, UA i ET, test `check_site.py` przechodzi.

## 2. Abstrakt
Obecnie hero pokazuje rysunek SVG generowany w JS: srebrne sylwetki puszek 200–500 ml w skali. Właściciel dostarczył 3 zdjęcia (1600 × 900) z puszkami matt silver/white/black na podstawce „PW GLOBAL”, na tle linii produkcyjnej. Na zdjęciach po prawej był wpisany polski tekst („Puszki 330 ml Regular…”), który na stronie EN/UA/ET byłby niezrozumiały — dlatego zdjęcia są przycięte do 1120 × 840 (bez tekstu), a podpis formatu jest dodany w HTML i tłumaczony. Zdjęcia pokazują kolory biały i czarny także dla 250 ml i 330 ml, których nie ma w tabeli stocku — podpisy podają tylko format, nie kolory; tabela stocku bez zmian.

## 3. Cel
- **Cele:** 3 zdjęcia w hero, automatyczna zmiana co ~4 s z płynnym przejściem, kropki do ręcznego wyboru, podpis formatu w każdym języku.
- **Poza zakresem:** zmiany tabeli stocku, kolorów w ofercie, innych sekcji; format WebP/AVIF.
- **Kryteria sukcesu:** wszystkie 3 wersje językowe pokazują te same zdjęcia; brak polskiego tekstu na zdjęciach; strona działa bez JS (widać pierwsze zdjęcie); użytkownik z „ogranicz ruch” nie ma automatycznej zmiany.

## 4. Inwentarz artefaktów
- `src/img/cans-250.jpg`, `cans-330.jpg`, `cans-500.jpg` — do utworzenia (przycięte, JPEG q78, ~145 KB)
- `src/en.html` — do zmiany: markup hero, CSS, JS (usunięty generator SVG, dodany pokaz)
- `build.py` — do zmiany: kopiowanie `src/img` → `dist/img`; tłumaczenia UA podpisów/alt
- `lang_et.py` — do zmiany: tłumaczenia ET
- `tests/check_site.py` — do zmiany: bramka „każdy `<img src>` ma plik w `dist/`”

## 5. Zmiany w domenie funkcjonalnej
- Stan obecny: SVG sylwetek 6 formatów z podpisami.
- Stan docelowy: kadr 4:3 z zaokrągleniem, zdjęcia nakładają się z przejściem przez przenikanie; podpis w rogu (np. „330 ml standard”); kropki pod spodem.
- Przypadki brzegowe: brak JS → widoczne pierwsze zdjęcie; `prefers-reduced-motion` → bez autoodtwarzania; karta w tle → animacja i tak tania (zmiana klasy); telefon → zdjęcie pod tekstem na pełną szerokość.
- Ścieżki obrazów bezwzględne (`/img/...`), bo UA i ET są w podfolderach.
- Pierwsze zdjęcie ładowane od razu, pozostałe `loading="lazy"`; podane `width`/`height`, żeby strona nie skakała.

## 6. Ścieżka krytyczna
Przycięcie zdjęć → markup + CSS + JS w `src/en.html` → kopiowanie w `build.py` → tłumaczenia UA/ET → test → podgląd lokalny (desktop + telefon) → zgoda właściciela → push.

## 7. Bramki kontrolne
| Bramka | Warunek | Weryfikacja | Blokuje |
|--------|---------|-------------|---------|
| Build/spójność | PASS | `python3 tests/check_site.py` | commit |
| Obrazy | każdy `<img src>` w EN/UA/ET ma plik w `dist/` | test | commit |
| Treść | 3 zdjęcia w hero w każdej wersji, podpisy przetłumaczone | grep `dist/` | commit |
| Ręczna | przenikanie działa, kropki działają, telefon OK | podgląd lokalny | push |
| Na żywo | `/img/cans-330.jpg` zwraca 200 | `curl` | zamknięcie |
| **Negatywna** | brak `id="lineup"` (stary SVG) i brak polskiego tekstu na stronie EN | test/grep | commit |

## 8. Oczekiwany wynik
Hero bardziej „żywe”, pokazuje realny produkt. Waga strony +~430 KB (2 zdjęcia ładowane leniwie). Rollback: `git revert` + push.

## 9. Informacje dodatkowe
- Odrzucone: wstawienie zdjęć z polskim tekstem (niezrozumiałe dla klientów EN/UA/ET); zostawienie SVG obok zdjęć (za ciasno).
- Otwarte pytanie: czy 250 ml i 330 ml w kolorze białym/czarnym mają trafić do tabeli stocku (obecnie 250 ml tylko silver, 330 ml standard silver i black).
