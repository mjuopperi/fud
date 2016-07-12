var Cookies = require('js-cookie');

function getPort() {
  return window.location.port != '' ? ':' + window.location.port : '';
}

function getDomainName() {
  var domain = _(window.location.hostname).split('.').takeRight(2).join('.');
  if (!_.startsWith(domain, 'fud')) return 'localhost';
  else return domain;
}

function getBaseUrl() {
  return window.location.protocol + '//' + getDomainName() + getPort();
}

function getApiUrl() {
  return window.location.protocol + '//api.' + getDomainName() + getPort();
}

function getRestaurantUrl(subdomain) {
  return window.location.protocol + '//' + subdomain + '.' + getDomainName() + getPort();
}

function getSubdomain() {
  return _(window.location.hostname).split('.').first();
}

function cookieDomain() {
  var domain = getDomainName();
  return domain === 'localhost' ? '' : domain
}

function setAuthToken(token) {
  Cookies.set('authToken', token, { domain: cookieDomain() });
}

function getAuthToken() {
  return Cookies.get('authToken');
}

function removeAuthToken() {
  Cookies.remove('authToken', { domain: cookieDomain() });
}

function authTokenExists() {
  return getAuthToken() !== undefined;
}

exports.getApiUrl = getApiUrl;
exports.getRestaurantUrl = getRestaurantUrl;
exports.getBaseUrl = getBaseUrl;
exports.getSubdomain = getSubdomain;
exports.setAuthToken = setAuthToken;
exports.getAuthToken = getAuthToken;
exports.removeAuthToken = removeAuthToken;
exports.authTokenExists = authTokenExists;