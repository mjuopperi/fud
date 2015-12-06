require('./_header');
require('./lib/jquery.validate');

const apiUrl = '/api/restaurants/';
const errorTexts = {
  unauthorized: 'You need to be logged in to register a restaurant.',
  subdomainInUse: 'Subdomain is already in use.',
  default: 'Something went wrong. Please try again.'
};
const validationSettings = {
  rules: {
    name: {
      required: true
    },
    subdomain: {
      required: true,
      subdomain: true,
      remote: '/api/restaurants/validate-subdomain'
    }
  },
  ignore: '.ignore',
  errorClass: 'invalid',
  success: function(label) {
    label.addClass('valid')
  },
  submitHandler: function(form, e) {
    register(e);
  },
  onfocusout: function(element) {
    $(element).valid();
  }
};
$.validator.addMethod('subdomain', function(value, element) {
  return /^[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?$/.test(value);
}, 'Only lower case letters, numbers and dashes are allowed.');

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

function updateSubdomainInfo() {
  var subdomain = $(this).val();
  if (subdomain !== '') {
    $('p.subdomain-info span.name').text($(this).val());
  } else {
    $('p.subdomain-info span.name').text('<name>');
  }
}

$(function() {
  $('input[name=name]').focus();
  $('#register').validate(validationSettings);
  $('input[name=subdomain]').keyup(updateSubdomainInfo);
});