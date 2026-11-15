# pwglobaltrading.com

Statyczna strona firmowa PW Global Trading OÜ (dostawca aluminiowych puszek i wieczek do napojów), hostowana na Netlify.
Projekt prowadzony wg metodyki Rondo / Context Driven Development (workwithrondo.com) — zasady w [MANIFEST.md](MANIFEST.md).

## Stan obecny (tu i teraz)

**Domeny:** pwglobaltrading.com (główna, + www); pwglobaltrading.eu i www → 301 na .com.

**Wersje językowe:** EN `/`, UA `/ua/`, ET `/et/` — ta sama struktura sekcji w każdej. Polityka prywatności tylko EN (`/privacy.html`).

**Sekcje strony (w kolejności):**
1. Hero — dostawca puszek i wieczek
2. `#cans` — puszki z magazynu (tabela formatów, paletyzacja 1180 × 1250)
3. `#lids` — wieczka (kolorowe zawleczki i znakowanie od 2 mln szt.)
4. `#print` — nadruk na puszce (formaty 200–500 ml, wykończenia, efekty)
5. `#about` — o nas
6. Zamawianie i dostawa
7. `#faq` — FAQ
8. `#contact` — formularz zapytania (Netlify Forms `quote`, powiadomienia e-mail)

**Architektura:**
- `src/en.html` — źródło strony (EN), jedyne miejsce edycji treści i wyglądu
- `build.py` — buduje `dist/`: EN, UA (tłumaczenia w liście `UA`), ET (z `lang_et.py`), polityka prywatności, `_redirects`, `robots.txt`, `sitemap.xml`
- `lang_et.py` — tłumaczenia ET, wyrównane indeksami z listą `UA`
- `dist/` — publikowany folder (Netlify `publish = "dist"`, bez komendy build — `dist/` jest commitowany)
- `tests/check_site.py` — bramki kontrolne (build + spójność wersji językowych)

**Ścieżka krytyczna zmiany:** edycja `src/en.html` + tłumaczenia UA/ET → `python3 tests/check_site.py` (PASS) → commit (z `dist/`) → push na `main` → Netlify publikuje automatycznie → weryfikacja na żywej stronie.

## Specyfikacje

| Nr | Tytuł | Status |
|----|-------|--------|
| [000](specs/000-szablon.md) | Szablon specyfikacji | szablon |

## Historia

Zob. [CHANGELOG.md](CHANGELOG.md).
