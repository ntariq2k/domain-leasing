/**
 * Netlify Edge Function — host-based routing.
 * For every lease domain, rewrites / to /sites/<domain>/index.html
 * so each domain gets its own fully static, SEO-optimised page.
 * All other paths (sitemap.xml, robots.txt, blog-data.json, assets) pass through.
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

export default async (request, context) => {
  const rawHost = (request.headers.get('host') || '').toLowerCase();
  const host    = rawHost.replace(/^www\./, '');
  const path    = new URL(request.url).pathname;

  // Only rewrite root requests for known lease domains
  if (!LEASE_DOMAINS.has(host)) return;
  if (path !== '/' && path !== '/index.html') return;

  return context.rewrite(`/sites/${host}/index.html`);
};

export const config = { path: '/*' };
