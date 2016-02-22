require('./_header');
var util = require('./_util');
var uiUtil = require('./_uiUtil');

const apiUrl = util.getApiUrl();
const errorTexts = {
  invalidCredentials: 'Invalid username or password.',
  default: 'Something went wrong. Please try again.'
};

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
  var submitButton = $('#login').find('button[type=submit]');
  uiUtil.showProgressIndicator(submitButton);
  var request = loginRequest(getInput());
  request.done(handleSuccess);
  request.fail(handleErrors);
  request.always(function() { uiUtil.hideProgressIndicator(submitButton) });
}

function redirectToUserPage() {
  window.location = '/profile'
}

function handleSuccess(data) {
  util.setAuthToken(data.auth_token);
  redirectToUserPage();
}

function handleErrors(errors) {
  if (errors.status == 400) {
    $('#error').find('p').text(errorTexts.invalidCredentials).parent().show();
  } else {
    $('#error').find('p').text(errorTexts.default).parent().show();
  }
}

$(function() {
  $('input[name=username]').focus();
  $('#login').submit(logIn);
});