# NNN — Tytuł zmiany

Status: szkic | zamknięta | wdrożona  ·  Data: RRRR-MM-DD

## 1. TL;DR
1–3 zdania: co się zmienia, dla kogo, jak potwierdzimy wynik.

## 2. Abstrakt
3–15 zdań: stan obecny, problem/luka, uzasadnienie, historia decyzji. Bez powtarzania TL;DR.

## 3. Cel
- **Cele:** co musi zostać osiągnięte (weryfikowalne).
- **Poza zakresem:** czego świadomie nie robimy.
- **Kryteria sukcesu:** warunki oznaczające „gotowe”.

## 4. Inwentarz artefaktów
Stan każdego: istnieje / do utworzenia / do zmiany / do usunięcia / [DO USTALENIA].
- **System:** `src/en.html`, `build.py`, `lang_et.py`, `dist/`, `netlify.toml`, Netlify (formularze, przekierowania)
- **Dane:** treści, tabele produktów, zdjęcia
- **Organizacja:** właściciel, dostawcy materiałów (np. zdjęcia), domeny/DNS

## 5. Zmiany w domenie funkcjonalnej
Zachowanie strony, nie plan implementacji: stan obecny → docelowy, reguły biznesowe, przypadki brzegowe (telefon, brak JS, inne języki), wpływ na dane/SEO/przekierowania.

## 6. Ścieżka krytyczna
Najkrótsza droga do działającej zmiany: cel, minimalny zakres, kolejność dowodów, warunek ukończenia.

## 7. Bramki kontrolne
| Bramka | Warunek zaliczenia (bez interpretacji) | Weryfikacja | Blokuje |
|--------|----------------------------------------|-------------|---------|
| Build/spójność | `tests/check_site.py` → PASS | komenda | commit |
| Treść | np. tekst X obecny w EN/UA/ET | grep w `dist/` | commit |
| Na żywo | np. `curl` pwglobaltrading.com zawiera X | komenda | zamknięcie |
| Ręczna | wygląd na telefonie i desktopie | zrzut ekranu | zamknięcie |
| **Negatywna** | czego strona NIE może robić (np. martwy link, angielski tekst w UA) | test | commit |

## 8. Oczekiwany wynik
Efekt bezpośredni, mierzalny (metryka i horyzont), skutki uboczne, rollback (czy i jakim kosztem — zwykle `git revert` + push).

## 9. Informacje dodatkowe
Odrzucone alternatywy z powodami, zaakceptowany dług techniczny, zależności zewnętrzne, źródła, otwarte pytania.
