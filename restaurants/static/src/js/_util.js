
function getPort() {
  return window.location.port != '' ? ':' + window.location.port : '';
}

function getDomainName() {
  var parts = window.location.hostname.split('.');
  return parts[parts.length - 1]
}

function getApiUrl() {
  return window.location.protocol + '//api.' + getDomainName() + getPort();
}

function getRestaurantUrl(subdomain) {
  return window.location.protocol + '//' + subdomain + '.' + getDomainName() + getPort();
}

exports.getApiUrl = getApiUrl;
exports.getRestaurantUrl = getRestaurantUrl;
