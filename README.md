# pwglobaltrading.com

Static website of PW Global Trading OÜ, hosted on Netlify.

- `src/en.html` – English page (source)
- `build.py` – builds `dist/`: EN page, Ukrainian page (translations inside), privacy policy, redirects, robots.txt, sitemap
- `dist/` – published folder (Netlify `publish = "dist"`, no build command)

Update: edit `src/en.html` / `build.py`, run `python3 build.py`, commit and push. Netlify deploys automatically.
