/**
 * lang_switch.js
 * Dynamically updates language-switch links to keep the user on the
 * equivalent sub-page instead of always jumping to the index.
 *
 * Strategy:
 *   - Read the already-resolved <link rel="alternate"> hrefs that MkDocs
 *     generates – they point to each language's index.html and therefore
 *     give us the absolute URL of every language root.
 *   - Both zh and en sites share the same page hierarchy, so the path
 *     segment after the language root is identical for equivalent pages.
 *   - Replace each selector link's href with  <lang_root> + <relative_page>.
 */
(function () {
  var zhAlt = document.querySelector('link[rel="alternate"][hreflang="zh"]');
  var enAlt = document.querySelector('link[rel="alternate"][hreflang="en"]');
  if (!zhAlt || !enAlt) return;

  // Derive language roots by stripping "index.html" from the resolved URLs.
  var zhRoot = zhAlt.href.replace(/index\.html$/, '');
  var enRoot = enAlt.href.replace(/index\.html$/, '');

  var currentUrl = window.location.href;

  // Determine which language root the current page belongs to.
  // English root is nested inside zh root (site/en/), so check it first.
  var pagePath;
  if (currentUrl.startsWith(enRoot)) {
    pagePath = currentUrl.slice(enRoot.length);   // e.g. "ToolBox/AddItem.html"
  } else if (currentUrl.startsWith(zhRoot)) {
    pagePath = currentUrl.slice(zhRoot.length);   // e.g. "ToolBox/AddItem.html"
  } else {
    return; // cannot determine position, leave links unchanged
  }

  if (!pagePath) pagePath = 'index.html';

  // Update every language selector anchor.
  document.querySelectorAll('a.md-select__link[hreflang]').forEach(function (link) {
    var lang = link.getAttribute('hreflang');
    if (lang === 'zh') {
      link.setAttribute('href', zhRoot + pagePath);
    } else if (lang === 'en') {
      link.setAttribute('href', enRoot + pagePath);
    }
  });
})();
