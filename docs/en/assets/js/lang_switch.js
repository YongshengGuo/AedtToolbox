/**
 * lang_switch.js  (English site copy – identical logic)
 * See docs/assets/js/lang_switch.js for full comments.
 */
(function () {
  var zhAlt = document.querySelector('link[rel="alternate"][hreflang="zh"]');
  var enAlt = document.querySelector('link[rel="alternate"][hreflang="en"]');
  if (!zhAlt || !enAlt) return;

  var zhRoot = zhAlt.href.replace(/index\.html$/, '');
  var enRoot = enAlt.href.replace(/index\.html$/, '');

  var currentUrl = window.location.href;

  var pagePath;
  if (currentUrl.startsWith(enRoot)) {
    pagePath = currentUrl.slice(enRoot.length);
  } else if (currentUrl.startsWith(zhRoot)) {
    pagePath = currentUrl.slice(zhRoot.length);
  } else {
    return;
  }

  if (!pagePath) pagePath = 'index.html';

  document.querySelectorAll('a.md-select__link[hreflang]').forEach(function (link) {
    var lang = link.getAttribute('hreflang');
    if (lang === 'zh') {
      link.setAttribute('href', zhRoot + pagePath);
    } else if (lang === 'en') {
      link.setAttribute('href', enRoot + pagePath);
    }
  });
})();
