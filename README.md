# Home Accessibility Solutions

One-page site for David Edge's home accessibility business in Springfield, MO.

- `src/partials/` holds the content, one file per section. `src/site.css` holds every color and font.
- `src/build.py` puts the pages together: run `python3 src/build.py`, then commit `public/`.
- `public/` is the finished site that Cloudflare serves. Don't edit it by hand.
- Pages: Home, Services, Who We Help, Our Work, How It Works, Paying for It, For Care Teams, About David. Add a page in the `PAGES` and `NAV` lists in `build.py`.
- `wrangler.jsonc` deploys `public/` as static assets on Cloudflare Workers.

## Cloudflare settings
- Workers (Git): build command empty, deploy command `npx wrangler deploy`.
- Pages (Git): framework "None", build command empty, output directory `public`.

## Before launch
- Confirm final business name and domain. It must match the Google Business Profile exactly.
- Confirm with David: free home visit, bathroom grab bars, completion photos for referral partners, retrofit list.
- Add David's photo and real retrofit install photos.
