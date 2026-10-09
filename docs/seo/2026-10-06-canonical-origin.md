# Canonical origin and internal links — 2026-10-06

Evidence: owner-supplied Ahrefs export landandwatercreations_05-oct-2026_duplicate-p_2026-10-06_15-33-13.csv. The October 5 crawl contains 116 indexable HTTP 200 URLs, no canonical tags, 29 paths and 29 content hashes each repeated four times across HTTP/HTTPS and www/non-www. This is crawl evidence, not a fresh production response measurement.

Preferred origin: https://landandwatercreations.com, matching the existing sitemap. This technical change supports discovery/consolidation of existing pond, landscape and outdoor-living service/project pages; it adds no business or horticultural claims.

## Implementation
- Cloudflare Worker redirects requests on either production hostname to HTTPS/non-www with HTTP 308. Path, query, method and body are preserved. Preferred-origin and preview/local requests pass through to the existing static assets binding. Worker-first routing ensures existing files do not bypass the host check. Requests now invoke Worker code; account limits/billing for Worker requests apply.
- 31 existing HTML pages (including the pending Orangedale page) have exactly one absolute canonical in the head. Existing page paths are preserved.
- 742 known internal HTML anchor targets point directly to the existing extensionless routes. Fragments/query parameters remain intact; external, email, phone, script, asset and form URLs are preserved.
- No sitemap additions, content rewrite or CSS changes. The pending pond PR already supplies its new sitemap entry.

## Review dependency
Based on PR #2 head 5daa2f46f424d6677b9218f3ad7b46b13753810b to avoid overwriting that work. Review as a stacked PR targeting seo/water-features-orangedale-pond; after #2 is merged, retarget this PR to main and check the diff. No production merge/deployment is performed here.

## Validation and remaining checks
- node --test worker.test.mjs: 15 passing redirect/pass-through tests, including query strings and preview hosts.
- python validate-seo.py: 31 single canonical tags, valid known internal link targets, 27 unique sitemap URLs. All non-anchor attributes excluding canonical tags match PR #2, including iframe forms, scripts, tracking, images and styles.
- git diff --check passes.
- Wrangler 4.148.0 deploy --dry-run successfully bundled the Worker and recognized the ASSETS binding. Local Wrangler preview could not start because this environment returned uv_interface_addresses system error 1; runtime/browser verification must use the Cloudflare preview and production after approval.
- No test lead submitted; email/SMS delivery and conversion events require an owner test after deployment.
- Confirm both production hostnames remain routed to this Worker. After approval/deployment, GET all four variants of /, /water-features and /contact-us with a query string. Three alternates must redirect to HTTPS/non-www, final pages must return 200, and assets/forms must render normally. Existing .html redirects may add a second hop for old links; normal internal links bypass them.
- Ahrefs connector has no start-crawl operation, and its issues endpoint last reported zero API units. Trigger New crawl in Ahrefs after deployment. Review duplicate groups, internal redirect links and remaining genuine heading/metadata issues after the crawl; compare qualified organic leads and GSC metrics over multiple weeks, without claiming ranking gains.

Sources: https://developers.cloudflare.com/workers/static-assets/routing/worker-script/ and https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
