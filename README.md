# Home Accessibility Solutions

One-page site for David Edge's home accessibility business in Springfield, MO.

- `public/` holds the site: `index.html` and `img/`. Plain HTML and CSS, no build step.
- `wrangler.jsonc` deploys `public/` as static assets on Cloudflare Workers.

## Cloudflare settings
- Workers (Git): build command empty, deploy command `npx wrangler deploy`.
- Pages (Git): framework "None", build command empty, output directory `public`.

## Before launch
- Confirm final business name and domain. It must match the Google Business Profile exactly.
- Confirm with David: free home visit, bathroom grab bars, completion photos for referral partners, retrofit list.
- Add David's photo and real retrofit install photos.
