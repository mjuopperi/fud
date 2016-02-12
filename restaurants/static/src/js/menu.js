require('./_header');
var util = require('./_util');

function buildTemplate() {
  return _.template(
    $("script.template").html()
  );
}

function setListeners() {
  $(".menus h1").on( "click", function() {
    $(".menu").removeClass("active-menu");
    $(".menu").eq($(this).index()).addClass("active-menu");
    storeActiveMenu($(this).index())
  });
}

function renderMenu(data) {
  const template = buildTemplate();
  var index = retrieveActiveMenu();
  $(".main").html(template(data));
  $(".menu").eq(index).addClass("active-menu");
}

function retrieveActiveMenu() {
  return sessionStorage.getItem('active-menu') === null ? 0 : sessionStorage.getItem('active-menu');
}

function storeActiveMenu(index) {
  sessionStorage.setItem('active-menu', index);
}

function getMenu() {
  const apiUrl = util.getApiUrl();
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/restaurants/fudu/menus',
    success: renderMenu
  });
}

function init() {
  _.templateSettings.variable = "restaurant";
  getMenu().then(setListeners);
}

$(function() {
  init();
});
