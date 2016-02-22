var util = require('./_util');

const apiUrl = util.getApiUrl();
const loginElem = $('<h2/>').append($('<a/>', {'href': '/login', 'text': 'Log in'}));
const signUpElem = $('<h2/>').append($('<a/>', {'href': '/signup', 'text': 'Sign up'}));

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
     .append($('<li/>').append($('<a/>', {href: '/profile',text: 'Profile'})))
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
  var request = userInfoRequest(localStorage.getItem('authToken'));
  exports.userInfo = request;
  request.done(renderUser);
  request.fail(handleAuthError)
}

function handleAuthError(e) {
  localStorage.removeItem('authToken');
}

function loggedIn() {
  return localStorage.getItem('authToken') !== null;
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
    localStorage.removeItem('authToken');
    window.location = '/login';
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
  if (loggedIn()) {
    getUserInfo();
  } else {
    renderDefaults();
  }
  $('.user').on('click', '.logout', logout);
  $('header').on('click', '.user.logged-in h2, .user.logged-in i', toggleUserMenu);
  $(document).click(hideUserMenu);
});

