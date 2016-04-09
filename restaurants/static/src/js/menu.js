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

function readMenu(context) {
  var $menu = $(context).parent().parent();
  var menu = {
    content: [],
    restaurant: subdomain,
    id: Number($($menu).attr("data-id")),
    title: $(".active").text() // change to val() after converting to input element
  }
  var categories = $($menu).find(".category");
  _.map(categories, function(c) {
    var category = {
      name: $(c).find("h3 input").val(),
      items: []
    };
    var menuItems = $(c).find(".menu-items li");
    _.map(menuItems, function(item) {
      category.items.push({
        name: $(item).find(".item-name").val(),
        price: $(item).find(".item-price").val(),
        description: $(item).find(".item-description").text(),
        allergens: $(item).find(".item-allergens").text().split(" ,")
      })
    })
    menu.content.push(category);
  })
  return menu;
}

function saveMenu() {
  var data = readMenu(this);
  $.ajax({
    type: 'PUT',
    url: apiUrl + '/restaurants/' + subdomain +  '/menus/' + data.id,
    data: JSON.stringify(data),
    contentType: "application/json",
    dataType: "json",
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function deleteMenu() {
  var id = $(this).parent().parent().attr("data-id");
  $.ajax({
    type: 'DELETE',
    url: apiUrl + '/restaurants/' + subdomain +  '/menus/' + id,
    headers: {Authorization: 'Token ' + util.getAuthToken()}
  });
}

function init() {
  getMenu().then(function(data) {
    var menus = data.menus;
    renderMenuTitles(menus);
    renderMenuContents(menus);
    setActiveMenu(getActiveMenuId());
  });
}

function setEditable() {
  $(this).attr('contenteditable', 'true');
  $(this).focus();
}

$(function() {
  init();
  $('section').on('click', '.menu-title', toggleMenu);
  $('section').on('click', '.save-menu', saveMenu);
  $('section').on('click', '.delete-menu', deleteMenu);
  $('section').on('click',  '.menu-title span', setEditable);
});
