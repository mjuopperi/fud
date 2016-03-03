require('./_header');
var util = require('./_util');
var menuTemplate = require('./templates/_menuTemplate');

function buildTemplate() {
  return _.template(
    menuTemplate.Menu
  );
}

function getRestaurantSubdomain() {
  return window.location.host.split('.')[0];
}

function setListeners() {
  $(".menus li").on( "click", function() {
    // desktop
    $(".menu").removeClass("active-menu");
    $(".menu").eq($(this).index()).addClass("active-menu");
    $(this).parent().find(".active-menu-title").removeClass("active-menu-title");
    $(this).find("span").addClass("active-menu-title")
    // mobile
    if(Number(retrieveActiveMenu()) === $(this).index()) {
      $(".categories").eq($(this).index()).toggleClass("active-menu");
    } else {
      $(".categories").removeClass("active-menu");
      $(".categories").eq($(this).index()).addClass("active-menu");
    }
    // store active menu
    storeActiveMenu($(this).index())
  });
}

function renderMenu(data) {
  const template = buildTemplate();
  var index = retrieveActiveMenu();
  $(".main").html(template(data));
  $(".menu").eq(index).addClass("active-menu");
  $(".menus li h1").eq(index).find("span").addClass("active-menu-title");

  // mobile
  $(".categories").eq(index).addClass("active-menu");
}

function retrieveActiveMenu() {
  return sessionStorage.getItem('active-menu') === null ? 0 : sessionStorage.getItem('active-menu');
}

function storeActiveMenu(index) {
  sessionStorage.setItem('active-menu', index);
}

function getMenu() {
  const apiUrl = util.getApiUrl();
  const subdomain = getRestaurantSubdomain();
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/restaurants/' + subdomain +  '/menus',
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
