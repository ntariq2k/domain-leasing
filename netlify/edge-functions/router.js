/**
 * Netlify Edge Function — host-based routing via fetch().
 * Rewrites root requests for each lease domain to /sites/<domain>/index.html
 * by fetching the file from the Netlify origin (avoids context.rewrite() failures).
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

  if (!LEASE_DOMAINS.has(host)) return;
  if (path !== '/' && path !== '/index.html') return;

  // Build the origin URL for the static per-domain file.
  // Netlify's origin is always accessible via the deploy URL (set as env var)
  // or by constructing a request to the same host with a rewritten path.
  const originBase = Netlify.env.get('URL') || `https://${request.headers.get('host')}`;
  const targetUrl  = `${originBase}/sites/${host}/index.html`;

  try {
    const res = await fetch(targetUrl, {
      headers: { 'x-forwarded-host': host },
    });
    if (!res.ok) return; // fall through to _redirects catch-all on error
    const body = await res.text();
    return new Response(body, {
      status: 200,
      headers: {
        'content-type': 'text/html; charset=utf-8',
        'cache-control': 'public, max-age=3600, stale-while-revalidate=86400',
        'x-served-by': 'edge-router',
      },
    });
  } catch {
    return; // fall through on any fetch error
  }
};

export const config = { path: '/*' };
