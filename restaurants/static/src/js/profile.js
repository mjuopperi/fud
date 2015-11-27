var header = require('./_header');
var util = require('./_util');

const apiUrl = util.getApiUrl();

function initPage(user) {
  $('h1.welcome').append(', ' + user.username + '!');
  $('input[name="email"]').val(user.email);
}

function renderRestaurants(restaurants) {
  console.log("Restaurants: ", restaurants)
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

function restaurantsRequest(authToken) {
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/restaurants/owned/',
    headers: {Authorization: 'Token ' + authToken}
  });
}

function getRestaurants() {
  var request = restaurantsRequest(localStorage.getItem('authToken'));
  request.done(renderRestaurants)
}

function nope() {
  $('.wrapper > section').css({
    'background': 'url(http://i.giphy.com/uVM1AZwC3AxYA.gif) no-repeat center',
    'background-size': 'cover'
  });
  setTimeout(unNope, 5000)
}

function unNope() {
  $('.wrapper > section').css({
    'background': '#fff'
  });
}

function changeEmail(e) {
  e.preventDefault();
  nope()
}

function changePassword(e) {
  e.preventDefault();
  nope()
}

$(function() {
  header.userInfo.done(function(user) {
    initPage(user);
    getRestaurants(localStorage.getItem('authToken'));
  });

  $('#change-email').submit(changeEmail);
  $('#change-password').submit(changePassword);
});