require('./_header');
var util = require('./_util');
var menuTemplate = require('./templates/menuAdmin.html');

const apiUrl = util.getApiUrl();
const subdomain = util.getSubdomain();

function getActiveMenuId() {
  var storedMenuId = sessionStorage.getItem('activeMenu');
  var firstMenuId = $('.menus .menu').first().data('id');
  return !storedMenuId ? firstMenuId : storedMenuId;
}

function storeActiveMenuId(id) {
  sessionStorage.setItem('activeMenu', id);
}

function getMenu() {
  return $.ajax({
    type: 'GET',
    url: apiUrl + '/restaurants/' + subdomain +  '/menus'
  });
}

function renderMenuTitles(menus) {
  _.each(menus, function(menu) {
    $('.menu-titles').append(
      $('<li>').append(
        $('<h2>', {class: 'menu-title desktop', 'data-id': menu.id}).append(
          $('<span>').text(menu.title)
        )
      )
    )
  });
}

function renderMenuContents(menus) {
  var template = _.template(menuTemplate);
  _.each(menus, function (menu) {
    $("ul.menus").append(template(menu))
  });
}

function toggleMenu() {
  var id = $(this).data('id');
  setActiveMenu(id);
  storeActiveMenuId(id);
}

function setActiveMenu(id) {
  var activeMenu = $('.menus').find('li[data-id="' + id + '"]');
  var activeTitles = $('.menu-title[data-id="' + id + '"]');
  activeMenu.find('.categories').show();
  activeMenu.siblings().find('.categories').hide();
  $('.menu-title').removeClass('active');
  activeTitles.addClass('active');
}

function init() {
  getMenu().then(function(data) {
    var menus = data.menus;
    renderMenuTitles(menus);
    renderMenuContents(menus);
    setActiveMenu(getActiveMenuId());
  });
}

$(function() {
  init();
  $('section').on('click', '.menu-title', toggleMenu);
});
