var header = require('./_header');
var util = require('./_util');
var uiUtil = require('./_uiUtil');

const apiUrl = util.getApiUrl();

const errorTexts = {
  currentPassword: 'Current password is incorrect.',
  default: 'Something went wrong. Please try again.'
};

var user;

function initPage() {
  $('h1.welcome').append(', ' + user.username + '!');
  $('input[name="email"]').val(user.email);
}

function renderRestaurants(restaurants) {
  $('#restaurants ul').empty();
  restaurants.results.forEach(renderRestaurant);
}

function renderRestaurant(restaurant) {
  var restaurantElem = $('<li>').append(
                         $('<a>', {
                           href: util.getRestaurantUrl(restaurant.subdomain),
                           text: restaurant.name
                         }));
  $('#restaurants ul').append(restaurantElem);
}

function restaurantsRequest() {
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/restaurants/owned/',
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function getRestaurants() {
  var request = restaurantsRequest();
  request.done(renderRestaurants)
}

function toggleFormFields(form) {
  form.find('input').each(function() {
    $(this).prop('disabled', function(i, disabled) { return !disabled; });
  });
  form.find('.cancel, .save, .extra').toggleClass('hidden');
  form.find('input').first().focus();
}

function toggleForm() {
  toggleFormFields($(this).closest('form'));
}

function changePasswordRequest(data) {
  return $.ajax({
    type: 'POST',
    url: apiUrl + '/auth/password/',
    data: data,
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function changeEmailRequest(email) {
  var updated = _.clone(user);
  updated.email = email;
  return $.ajax({
    type: 'PUT',
    url: apiUrl + '/auth/me/',
    data: updated,
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function changeEmail(e) {
  e.preventDefault();
  var submitButton = $('#change-email').find('button[type=submit]');
  uiUtil.showProgressIndicator(submitButton);
  var request = changeEmailRequest($('input[name="email"]').val());
  request.done(handleEmailSuccess);
  request.fail(handleErrors);
  request.always(function() { uiUtil.hideProgressIndicator(submitButton) });
}

function handleEmailSuccess() {
  handleSuccess();
  var form = $('#change-email');
  toggleFormFields(form);
  uiUtil.showSuccesIndicator(form);
}

function changePassword(e) {
  e.preventDefault();
  var submitButton = $('#change-password').find('button[type=submit]');
  uiUtil.showProgressIndicator(submitButton);
  var request = changePasswordRequest({
    current_password: $('input[name="current-password"]').val(),
    new_password: $('input[name="new-password"]').val()
  });
  request.done(handlePasswordSuccess);
  request.fail(handlePasswordErrors);
  request.always(function() { uiUtil.hideProgressIndicator(submitButton) });
}

function handleSuccess() {
  $('#error').hide();
  $('input.invalid').removeClass('invalid');
}

function handlePasswordSuccess() {
  handleSuccess();
  var form = $('#change-password');
  form.find('input').each(function() {
    $(this).val('');
  });
  toggleFormFields(form);
  uiUtil.showSuccesIndicator(form);
}

function handleErrors() {
  $('#error').find('p').text(errorTexts.default).parent().show();
}

function handlePasswordErrors(errors) {
  if (errors.status == 400 && errors.responseJSON.current_password) {
    $('#error').find('p').text(errorTexts.currentPassword).parent().show();
    $('input[name="current-password"]').addClass('invalid');
  } else {
    handleErrors();
  }
}

$(function() {
  header.userInfo.done(function(result) {
    user = result;
    initPage();
    getRestaurants(util.getAuthToken());
  });

  $('button.change, button.cancel').click(toggleForm);
  $('#change-email').submit(changeEmail);
  $('#change-password').submit(changePassword);
});