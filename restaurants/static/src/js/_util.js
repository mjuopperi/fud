var Cookies = require('js-cookie');

function getPort() {
  return window.location.port != '' ? ':' + window.location.port : '';
}

function getDomainName() {
  return _(window.location.hostname).split('.').takeRight(2).join('.');
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

function setAuthToken(token) {
  Cookies.set('authToken', token, { domain: getDomainName() });
}

function getAuthToken() {
  return Cookies.get('authToken');
}

function removeAuthToken() {
  Cookies.remove('authToken', { domain: getDomainName() });
}

function authTokenExists() {
  return getAuthToken() !== undefined;
}

exports.getApiUrl = getApiUrl;
exports.getRestaurantUrl = getRestaurantUrl;
exports.getSubdomain = getSubdomain;
exports.setAuthToken = setAuthToken;
exports.getAuthToken = getAuthToken;
exports.removeAuthToken = removeAuthToken;
exports.authTokenExists = authTokenExists;