const apiUrl = '/api/auth/login/';
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
    url: apiUrl,
    data: data
  });
}

function logIn(e) {
  e.preventDefault();
  var request = loginRequest(getInput());
  request.done(handleSuccess);
  request.fail(handleErrors);
}

function redirectToUserPage() {
  window.location = '/me'
}

function handleSuccess(data) {
  storeAuthToken(data.auth_token);
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
  $('#login').submit(logIn);
});