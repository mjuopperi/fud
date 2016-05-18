var util = require('./_util');
util = require('./_util')

const apiUrl = util.getApiUrl();
const baseUrl = util.getBaseUrl();
const loginElem = $('<h2/>').append($('<a/>', {'href': baseUrl + '/login', 'text': 'Log in'}));
const signUpElem = $('<h2/>').append($('<a/>', {'href': baseUrl + '/signup', 'text': 'Sign up'}));

function renderDefaults() {
  if (window.location.pathname === '/login') $('header').find('.user').html(signUpElem);
  else if (window.location.pathname === '/signup') $('header').find('.user').html(loginElem);
  else $('header').find('.user').html(loginElem).append(signUpElem);
  $('header').find('.user').removeClass('logged-in');
}

function renderUser(user) {
  $('header').find('.user').addClass('logged-in').html(
    $('<h2/>').append($('<a/>', {text: user.username}))
  ).append($('<ul/>')
     .append($('<li/>').append($('<a/>', {href: baseUrl + '/profile',text: 'Profile'})))
     .append($('<li/>').append($('<a/>', {class: 'logout', text: 'Log out'})))
  ).append(
    $('<i>', {class: 'fa fa-bars'})
  )
}

function userInfoRequest(authToken) {
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/auth/me/',
    headers: {Authorization: 'Token ' + authToken}
  });
}

function getUserInfo() {
  var request = userInfoRequest(util.getAuthToken());
  exports.userInfo = request;
  request.done(renderUser);
  request.fail(handleAuthError)
}

function handleAuthError(e) {
  util.removeAuthToken();
}

function logoutRequest() {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/logout/',
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function logout(e) {
  e.preventDefault();
  logoutRequest().always(function() {
    util.removeAuthToken();
    window.location = baseUrl + '/login';
  });
}

function toggleUserMenu(e) {
  $('.user ul').toggle();
  e.stopPropagation();
}

function hideUserMenu() {
  $('.user ul').hide();
}

$(function() {
  if (util.authTokenExists()) {
    getUserInfo();
  } else {
    renderDefaults();
  }
  $('.user').on('click', '.logout', logout);
  $('header').on('click', '.user.logged-in h2, .user.logged-in i', toggleUserMenu);
  $(document).click(hideUserMenu);
});

