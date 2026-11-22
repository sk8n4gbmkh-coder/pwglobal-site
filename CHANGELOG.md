# CHANGELOG

Co faktycznie zostało zbudowane, wg dat. Wpisy do 2026-11-14 odtworzone z historii git.

## 2026-11-22
- Tabela puszek z magazynu: pełna lista kolorów wg listy od właściciela — 15 wierszy (dodane black matt dla 200/250 slim i 330 sleek, white matt dla 330 sleek/standard i 500 ml; „Black” → „Black matt”; „Black/white matt” rozbite na black matt i white matt). Spec [002](specs/002-kolory-w-tabeli-stocku.md).
- Dane palet wg tabeli na asaszi.pl: 200 ml slim paleta 1100 × 1200 × 2060; 250 ml slim 550 szt./warstwę, 9 350 szt./paletę; 500 ml wysokość palety 2174 mm.
- Hero: rysunek SVG formatów puszek zastąpiony pokazem 3 zdjęć (250 ml slim, 330 ml standard, 500 ml standard; matt silver/white/black), przenikanie co 4,5 s, kropki do wyboru, bez autoodtwarzania przy „ogranicz ruch”. Zdjęcia przycięte (bez polskiego napisu), podpisy i opisy alt w EN/UA/ET. Spec [001](specs/001-zdjecia-puszek-w-hero.md).
- `build.py` kopiuje `src/img/` do `dist/img/`; test sprawdza, że każdy obraz istnieje i stary SVG zniknął.

## 2026-11-15
- Wprowadzona metodyka Rondo / CDD: README (stan obecny), CHANGELOG, MANIFEST, `specs/` z szablonem, bramki kontrolne `tests/check_site.py`.

## 2026-11-14
- Usunięta sekcja „Multipack packaging / Shrink packs and trays” (`#packaging`) i link „Packaging” w menu — EN, UA, ET.

## 2026-10-30
- „Blank” zamiast „plain”; linia srebrnych puszek z odstępami w hero; palety 1180 × 1250.
- Wszystkie puszki z magazynu BPA-NI i bez PFAS (PPWR); scalony zdublowany wiersz 500 ml black matt.
- MOQ 2 mln wieczek dla kolorowych zawleczek i znakowania; skrócona notka o wieczkach.
- Formaty druku: 440 ml zamiast 473 ml.
- FAQ: skrócona lista krajów (bez „the” przed EU, UK, USA).

## 2026-10-29
- Nowa strona PW Global Trading (EN/UA) na Netlify, zamiast Wix.
- Wersja estońska (ET), ciaśniejszy nagłówek na telefonie.
- Przekierowanie pwglobaltrading.eu → pwglobaltrading.com.
