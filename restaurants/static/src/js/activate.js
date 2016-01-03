require('./_header');
var util = require('./_util');

const apiUrl = util.getApiUrl();
const errorTexts = {
  default: 'Something went wrong. Please try again.'
};

function activateAccount() {
  $('.spinner').show();
  $(this).prop('disabled', true);
  var request = activationRequest($(this).data('uid'), $(this).data('token'));
  request.done(handleSuccess);
  request.fail(handleErrors);
}

function activationRequest(uid, token) {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/activate/',
    data: {
      'uid': uid,
      'token': token
    }
  });
}

function handleSuccess() {
  $('.spinner').hide();
  $('.success').fadeIn(400);
  setTimeout(function() {
    window.location = '/login'
  }, 800)
}

function handleErrors() {
  $('.spinner').hide();
  $(this).prop('disabled', false);
  $('#error').find('p').text(errorTexts.default).parent().show();
}

$(function() {
  $('#activate-account').click(activateAccount)
});