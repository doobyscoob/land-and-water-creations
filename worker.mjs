const HOST = 'landandwatercreations.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // Scope redirects to the two production hosts; previews stay accessible.
    if ((url.hostname === HOST || url.hostname === `www.${HOST}`) &&
        (url.protocol !== 'https:' || url.hostname !== HOST)) {
      url.protocol = 'https:';
      url.hostname = HOST;
      url.port = '';
      // 308 preserves the method/body as well as the path and query string.
      return Response.redirect(url.href, 308);
    }
    return env.ASSETS.fetch(request);
  },
};
