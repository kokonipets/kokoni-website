# kokonipets.com

Static site, hosted on Vercel (project: kokoni-website).

- English pages: index.html, services.html, meet-us.html, faq.html, contact.html, compare-styles.html
- Chinese pages in zh-tw/ and zh-cn/ are GENERATED. Don't edit them by hand.
  After changing an English page or its I18N translations, run `python3 build.py`
  (needs `pip install beautifulsoup4`), then commit and push.
- Push to main = live site updates automatically.
