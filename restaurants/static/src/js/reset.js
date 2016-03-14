require('./_header');
require('./lib/jquery.validate');
var util = require('./_util');
var uiUtil = require('./_uiUtil');

const apiUrl = util.getApiUrl();
const validationSettings = {
  rules: {
    password: {
      required: true,
      minlength: 8
    }
  },
  messages: {
    password: {
      minlength: 'Password must be atleast 8 characters long.'
    }
  },
  errorClass: 'invalid',
  success: function(label) {
    label.addClass('valid')
  },
  submitHandler: function(form, e) {
    resetPassword(e);
  },
  onfocusout: function(element) {
    $(element).valid();
  }
};


function getInput() {
  var data = {};
  $("#reset-password").serializeArray().map(function(field){data[field.name] = field.value;});
  return data;
}

function passwordResetRequest(data) {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/password/reset/confirm/',
    data: data
  });
}

function resetPassword(e) {
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
  $('#reset-password').hide();
  $('.success').show();
}

function handleErrors(errors) {
  $('#error').show();
}

$(function() {
  $('input[name=new_password]').focus();
  $('#reset-password').validate(validationSettings);
});
