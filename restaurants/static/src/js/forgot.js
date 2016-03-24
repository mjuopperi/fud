require('./_header');
require('./lib/jquery.validate');
var util = require('./_util');
var uiUtil = require('./_uiUtil');

const apiUrl = util.getApiUrl();
const errorTexts = {
  default: 'Something went wrong. Please try again.',
  invalidEmail: 'Please enter a valid email.'
};

function getInput() {
  return { email: $('input[name="email"]').val() }
}

function passwordResetRequest(data) {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/password/reset/',
    data: data
  });
}

function sendResetEmail(e) {
  e.preventDefault();
  var submitButton = $('#reset-password').find('button[type=submit]');
  uiUtil.showProgressIndicator(submitButton);
  var request = passwordResetRequest(getInput());
  request.done(handleSuccess);
  request.fail(handleErrors);
  request.always(function() { uiUtil.hideProgressIndicator(submitButton) });
}

function handleSuccess() {
  $('p.info').hide();
  $('#error').hide();
  $('#forgot-password').hide();
  $('.success').show();
}

function invalidEmail(errors) {
  return errors.responseJSON.hasOwnProperty('email') && errors.responseJSON.email[0] == "Enter a valid email address.";
}

function handleErrors(errors) {
  if (invalidEmail(errors)) {
    $('#error').find('p').text(errorTexts.invalidEmail).parent().show();
  } else {
    $('#error').find('p').text(errorTexts.default).parent().show();
  }
}

$(function() {
  $('input[name=email]').focus();
  $('#forgot-password').submit(sendResetEmail);
});
