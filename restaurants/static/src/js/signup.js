require('./_header');
require('./lib/jquery.validate');
var util = require('./_util');

const apiUrl = util.getApiUrl();
const errorTexts = {
  usernameInUse: 'Username already in use.',
  default: 'Something went wrong. Please try again.'
};
const validationSettings = {
  rules: {
    username: {
      required: true,
      remote: apiUrl + '/restaurants/validate-username'
    },
    email: {
      required: true,
      emailAddress: true
    },
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
    signUp(e);
  },
  onfocusout: function(element) {
    $(element).valid();
  }
};

$.validator.addMethod('emailAddress', function(value, element) {
  return /^([\w-\.]+@([\w-]+\.)+[\w-]{2,})?$/.test(value);
}, 'Please enter a valid email.');

function getInput() {
  return {
    username: $('input[name="username"]').val(),
    email: $('input[name="email"]').val(),
    password: $('input[name="password"]').val()
  }
}

function signUpRequest(data) {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/register/',
    data: data
  });
}

function signUp(e) {
  e.preventDefault();
  var request = signUpRequest(getInput());
  request.done(handleSuccess);
  request.fail(handleErrors);
}

function redirectToLoginPage() {
  window.location = '/login'
}

function usernameInUse(errors) {
  return errors.responseJSON.hasOwnProperty('username') && errors.responseJSON.username[0].indexOf('unique') > -1;
}

function handleSuccess() {
  redirectToLoginPage();
}

function handleErrors(errors) {
  if (usernameInUse(errors)) {
    $('#error').find('p').text(errorTexts.usernameInUse).parent().show();
    $('input[name="username"]').addClass('invalid');
  } else {
    $('#error').find('p').text(errorTexts.default).parent().show();
  }
}

$(function() {
  $('input[name=username]').focus();
  $('#signup').validate(validationSettings);
});
