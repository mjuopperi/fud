const apiUrl = '/api/auth/register/';
const errorTexts = {
  usernameInUse: 'Username already in use.',
  default: 'Something went wrong. Please try again.'
};

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
    url: apiUrl,
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
  window.location = '/login#new'
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
  $('#signup').submit(signUp);
});
