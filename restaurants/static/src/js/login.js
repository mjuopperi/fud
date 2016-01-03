require('./_header');
var util = require('./_util');

const apiUrl = util.getApiUrl();
const errorTexts = {
  invalidCredentials: 'Invalid username or password.',
  default: 'Something went wrong. Please try again.'
};

function storeAuthToken(token) {
  localStorage.setItem('authToken', token);
}

function getInput() {
  return {
    username: $('input[name="username"]').val(),
    password: $('input[name="password"]').val()
  }
}

function loginRequest(data) {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/login/',
    data: data
  });
}

function logIn(e) {
  e.preventDefault();
  showLoader();
  var request = loginRequest(getInput());
  request.done(handleSuccess);
  request.fail(handleErrors);
}

function redirectToUserPage() {
  window.location = '/me'
}

function handleSuccess(data) {
  hideLoader();
  storeAuthToken(data.auth_token);
  redirectToUserPage();
}

function handleErrors(errors) {
  hideLoader();
  if (errors.status == 400) {
    $('#error').find('p').text(errorTexts.invalidCredentials).parent().show();
  } else {
    $('#error').find('p').text(errorTexts.default).parent().show();
  }
}

function showLoader() {
  $('.overlay').show();
  $('#login > button').prop('disabled', true);
}

function hideLoader() {
  $('.overlay').hide();
  $('#login > button').prop('disabled', false);
}

$(function() {
  $('input[name=username]').focus();
  $('#login').submit(logIn);
});