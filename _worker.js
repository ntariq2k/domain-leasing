/**
 * Cloudflare Pages Worker — per-domain routing.
 * Serves /sites/<domain>/index.html for each lease domain root request.
 * env.ASSETS.fetch() reads directly from the Pages static asset bundle —
 * no network round-trip, no mysterious fallbacks.
 */
const LEASE_DOMAINS = new Set([
  'nycreagent.com',
  'webuyqueens.com',
  'webuynycbuilding.com',
  'webuynycbuildings.com',
  'njsellersagent.com',
  'nycroofexperts.com',
  'nycpaintexperts.com',
  'nycreconsultant.com',
  'nycreconsultants.com',
]);

export default {
  async fetch(request, env) {
    const url  = new URL(request.url);
    const host = (request.headers.get('host') || '').toLowerCase().replace(/^www\./, '');
    const path = url.pathname;

    // Route lease domain root requests to their static pre-rendered page
    if (LEASE_DOMAINS.has(host) && (path === '/' || path === '/index.html')) {
      const assetUrl = new URL(`/sites/${host}/index.html`, url);
      return env.ASSETS.fetch(new Request(assetUrl.toString(), request));
    }

    // All other paths (sitemap.xml, robots.txt, blog-data.json, /sites/*, assets)
    // are served directly from the static bundle
    return env.ASSETS.fetch(request);
  },
};
