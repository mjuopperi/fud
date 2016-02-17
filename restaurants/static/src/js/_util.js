
function getPort() {
  return window.location.port != '' ? ':' + window.location.port : '';
}

function getDomainName() {
  if (window.location.hostname.indexOf('fud.fi') > -1) return 'fud.fi';
  else if (window.location.hostname.indexOf('localhost') > -1) return 'localhost';
  else {
    var parts = window.location.hostname.split('.');
    return parts[parts.length - 2]
  }
}

function getApiUrl() {
  return window.location.protocol + '//api.' + getDomainName() + getPort();
}

function getRestaurantUrl(subdomain) {
  return window.location.protocol + '//' + subdomain + '.' + getDomainName() + getPort();
}

function getAuthToken() {
  return localStorage.getItem('authToken');
}

exports.getApiUrl = getApiUrl;
exports.getRestaurantUrl = getRestaurantUrl;
exports.getAuthToken = getAuthToken;