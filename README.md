# locales-sandbox

A stand-in for `pdffiller/locales`, for testing promo localization (ACC-11785) without touching the
real repository, Crowdin or the CDN.

- `source/*.po` — what `pdffiller-php-promo-module` writes through its pull requests, as in `locales`.
- `translations/<lang>/<file>.json` — the "translators": `{"KEY": "translation"}`, by hand.
- `Manual run build` (`.github/workflows/manual_run_build.yml`) — the "build": like the real one, it
  writes `branches/<branch>/ga<run id>/<lang>/<file>.json` shaped `{"data": {…}, "meta": {…}}`,
  English from `source/`, every key a translation lacks as its English, every value through
  `json_decode`, and `de` always. Instead of S3 it commits the files here, so
  `https://raw.githubusercontent.com/serhiiAirslate/locales-sandbox/main/branches/` plays the CDN.

Point the promo module at it with:

```
LOCALES_GITHUB_REPOSITORY=serhiiAirslate/locales-sandbox
LOCALES_CDN_URL=https://raw.githubusercontent.com/serhiiAirslate/locales-sandbox/main/branches/
```
