require('./_header');
var util = require('./_util');
var uiUtil = require('./_uiUtil');

const apiUrl = util.getApiUrl();
const errorTexts = {
  default: 'Something went wrong. Please try again.'
};

function activateAccount() {
  var activateButton = $('#activate-account');
  uiUtil.showProgressIndicator(activateButton);
  var request = activationRequest($(this).data('uid'), $(this).data('token'));
  request.done(handleSuccess);
  request.fail(handleErrors);
  request.always(function() { uiUtil.hideProgressIndicator(activateButton) });
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
  $('.success').show();
  setTimeout(function() {
    window.location = '/login'
  }, 800)
}

function handleErrors() {
  $('#error').find('p').text(errorTexts.default).parent().show();
}

$(function() {
  $('#activate-account').click(activateAccount)
});