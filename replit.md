# Land & Water Creations

This is the existing static HTML, CSS, and JavaScript website. Keep its structure
and existing service-page styling; no framework or build step is required.

## Preview

Run the **Preview website** workflow, or `python3 scripts/preview.py`.
The development server listens on `0.0.0.0:5000` and serves `site/`.
Open `/outdoor-living` to view the outdoor living service page.
`/outdoorliving` redirects to that page. Clean URLs and `.html` URLs both work.

## Hosting and assets

The existing Cloudflare configuration serves `site/` directly. The preview
server is only for development; it does not replace the hosting configuration.
`site/_redirects` supplies the outdoor living alias for Cloudflare.
The optimized outdoor living photos live in `site/assets/outdoor-living/`.
Uploaded originals and generated verification output are excluded from Git and
deployment.

Production tracking is skipped on localhost and `.replit.dev` preview hosts.
The imported Google Tag Manager container includes a legacy message listener
that calls `window.log` on a parse error; loading it in the editor preview caused
uncaught errors. Production hosts retain the existing tracking configuration.
