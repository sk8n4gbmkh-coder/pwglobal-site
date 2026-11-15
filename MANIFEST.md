# Manifest inżynierski — pwglobaltrading.com

Zasady stosowane w każdej specyfikacji i każdej zmianie. Metodyka: Rondo / Context Driven Development (workwithrondo.com).

## Artefakty
- `README.md` — stan „tu i teraz”: sekcje strony, architektura, ścieżka krytyczna, lista specyfikacji ze statusem.
- `specs/NNN-nazwa.md` — zamiar zmiany („chciałbym”), w stałej strukturze 9 sekcji z `specs/000-szablon.md`.
- `CHANGELOG.md` — co faktycznie zbudowano, wg dat.
- `tests/check_site.py` — dowód, że działa. Spec i CHANGELOG nie są dowodem.

## Przebieg zmiany
1. Spec przed kodem: cel, czego nie robimy, bramki kontrolne. Drobna zmiana treści (literówka, liczba, jedno zdanie) może pominąć spec — wystarczy wpis w CHANGELOG.
2. Implementacja wg ścieżki krytycznej, bez prac pobocznych.
3. `python3 tests/check_site.py` musi dać PASS przed commitem.
4. Aktualizacja README (jeśli zmienia się stan/sekcje), CHANGELOG, statusu specu.
5. Publikacja (push na `main`) tylko za zgodą właściciela; zmiany grupujemy — darmowy plan Netlify ma limit publikacji.
6. Weryfikacja na żywej stronie wszystkich trzech wersji.

## Zasady techniczne
- Strona statyczna, bez frameworków i zależności; jedyne źródło treści to `src/en.html`.
- Każda zmiana treści trafia do wszystkich wersji: EN, UA (`build.py`), ET (`lang_et.py`, indeksy wyrównane z `UA`).
- Wszystkie wersje mają te same sekcje w tej samej kolejności; każdy link `#kotwica` musi mieć cel.
- Formularz kontaktowy zostaje na Netlify Forms (`name="quote"`, honeypot).
- Bez danych wrażliwych w repo — jest publiczne.
- Dane produktowe (formaty, palety, MOQ, certyfikaty) tylko z materiałów od właściciela, nie zgadujemy.

## Po każdej rundzie zmian
- Analiza bezpieczeństwa i regresji obecnej i wcześniejszych zmian (formularz, przekierowania, nagłówki, linki, zewnętrzne zasoby).
- Każde znalezisko = spec + test odtwarzający problem + wpis w CHANGELOG.

## Awaria
Najpierw naprawa, potem spec, wpis w CHANGELOG i test regresyjny odtwarzający błąd.
