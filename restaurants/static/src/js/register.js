require('./_header');

const apiUrl = '/api/restaurants/';
const errorTexts = {
  unauthorized: 'You need to be logged in to create a restaurant.',
  subdomainInUse: 'Subdomain is already in use.',
  default: 'Something went wrong. Please try again.'
};

function getInput() {
  var data = {};
  $("#register").serializeArray().map(function(field){data[field.name] = field.value;});
  return data;
}

function registerRequest(data) {
  return $.ajax({
    type: 'POST',
    url: apiUrl,
    data: data,
    headers: {Authorization: 'Token ' + localStorage.getItem('authToken')}
  });
}

function register(e) {
  e.preventDefault();
  var request = registerRequest(getInput());
  request.done(handleSuccess);
  request.fail(handleErrors);
}

function redirectToRestaurantPage(subdomain) {
  window.location = '/' + subdomain + '/admin'
}

function handleSuccess(data) {
  redirectToRestaurantPage(data.subdomain);
}

function handleErrors(errors) {
  if (errors.status == 400 && errors.responseText.indexOf('subdomain') > -1) {
    $('#error').find('p').text(errorTexts.subdomainInUse).parent().show();
    $('#register').find('input[name=subdomain]').addClass('invalid');
  } else if (errors.status == 401) {
    $('#error').find('p').text(errorTexts.unauthorized).parent().show();
  } else {
    $('#error').find('p').text(errorTexts.default).parent().show();
  }
}

$(function() {
  $('#register').submit(register);
  $('#register').on('keypress', '.invalid', function() {
    $(this).removeClass('invalid');
  })
});