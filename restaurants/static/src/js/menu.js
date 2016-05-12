require('./_header');
var util = require('./_util');
var menuTemplates = {
  user: require('./templates/menu.html'),
  admin: require('./templates/menuAdmin.html')
};

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
          $('<span placeholder="Title">').text(menu.title)
        )
      )
    )
  });
  if(isAdmin()) {
    $('.menu-title span').attr('contenteditable', true);
    $('.menu-titles').append(
      $('<li>').append(
        $('<button>', {class: 'add-menu button-text'}).text(' Add new menu').prepend($('<i>', {class: 'fa fa-plus', 'aria-hidden': 'true'}))
      )
    )
  }
}

function renderMenuContents(menus) {
  var template = _.template(
    isAdmin() ? menuTemplates.admin : menuTemplates.user
  );
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
  var $mobile = $(".menu-title.title.mobile.active");
  var $desktop = $(".menu-title.desktop.active");
  var title = $mobile.is(":visible") ? $mobile.text() : $desktop.text();
  var menu = {
    content: [],
    restaurant: subdomain,
    id: Number($($menu).attr("data-id")),
    title: title
  }
  var categories = $($menu).find(".category");
  _.map(categories, function(c) {
    var category = {
      name: $(c).find("h3 span").text(),
      items: []
    };
    var menuItems = $(c).find(".menu-items li");
    _.map(menuItems, function(item) {
      category.items.push({
        name: $(item).find(".item-name").text(),
        price: $(item).find(".item-price").text(),
        description: $(item).find(".item-description").text(),
        allergens: $(item).find(".item-allergens").text().split(" ,")
      })
    })
    menu.content.push(category);
  })
  return menu;
}

function updateMenu() {
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
  $(this).parent().parent().remove();
  $('.menu-titles').find("[data-id='" + id + "']").parent().remove();
  var firstMenuID = $('.menu-titles > li > h2').first().attr('data-id');
  setActiveMenu(firstMenuID);
}

function setAdmin(owner) {
  owner ? sessionStorage.setItem('owner', true) : sessionStorage.setItem('owner', false);
}

function isAdmin() {
  return sessionStorage.getItem('owner') === null ? false : JSON.parse(sessionStorage.getItem('owner'));
}

function refresh() {
  getMenu().then(function(data) {
    var menus = data.menus;
    $('.menu-titles').empty();
    $('.menus').empty();
    renderMenuTitles(menus);
    renderMenuContents(menus);
    setActiveMenu(getActiveMenuId());
  });
}

function toggleEdit() {
  setAdmin(!isAdmin());
  refresh();
}

function createMenu() {
  var menu = {
    content: [{
      name: '',
      items: [{
        name: '',
        price: '',
        description: '',
        allergens: ['']
      }]
    }],
    restaurant: subdomain,
    title: 'New menu'
  }

  $.ajax({
    type: 'POST',
    url: apiUrl + '/restaurants/' + subdomain +  '/menus/',
    data: JSON.stringify(menu),
    contentType: "application/json",
    dataType: "json",
    headers: {Authorization: 'Token ' + util.getAuthToken()},
    success: renderNewMenu
  });
}

function renderNewMenu(data) {
  $('.menu-titles > li:last').before(
    $('<li>').append(
      $('<h2>', {class: 'menu-title desktop', 'data-id': data.id}).append(
        $('<span placeholder="Title" contenteditable=true>').text(data.title)
      )
    )
  )
  var template = _.template(menuTemplates.admin);
  $("ul.menus").append(template(data))
  setActiveMenu(data.id);
}

function createCategory() {
  $(this).parent().find('.category:last').after(
    $('<li>', {class: 'category'}).append(
      $('<h3>', {class: 'category-name'}).append(
        $('<span placeholder="Category" contenteditable=true>'),
        $('<button>', {class: 'add-menu-item button-icon'}).append(
          $('<i class="fa fa-plus" aria-hidden=true>')
        ),
        $('<button>', {class: 'delete-category button-icon'}).append(
          $('<i class="fa fa-times" aria-hidden=true>')
        )
      ),
      $('<ul>', {class: 'menu-items'}).append(
        $('<li>').append(
          $('<div>', {class: 'menu-item-title'}).append(
            $('<h4 class="item-name" contenteditable=true placeholder="Name">'),
            $('<h4 class="item-price" contenteditable=true placeholder="0.0€">')
          ),
          $('<p class="item-description" contenteditable=true placeholder="Description">'),
          $('<p class="item-allergens" contenteditable=true placeholder="Allergens">'),
          $('<button>', {class: 'delete-item button-icon'}).append(
            $('<i class="fa fa-times" aria-hidden="true">')
          )
        )
      )
    )
  )
}

function deleteCategory() {
  $(this).parent().parent().remove();
}

function createMenuItem() {
  $(this).parent().parent().find('.menu-items').append(
    $('<li>').append(
      $('<div>', {class: 'menu-item-title'}).append(
        $('<h4 contenteditable=true placeholder="Name">', {class: 'item-name'}),
        $('<h4 contenteditable=true placeholder="0.0€">', {class: 'item-price'})
      ),
      $('<p contenteditable=true placeholder="Description">', {class: 'item-description'}),
      $('<p contenteditable=true placeholder="Allergens">', {class: 'item-allergens'}),
      $('<button>', {class: 'delete-item button-icon'}).append(
        $('<i class="fa fa-times" aria-hidden="true">')
      )
    )
  )
}

function deleteMenuItem() {
  $(this).parent().remove();
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
  $('section').on('click', '.save-menu', updateMenu);
  $('section').on('click', '.delete-menu', deleteMenu);
  $('section').on('click', '.edit-menu', toggleEdit);
  $('section').on('click', '.add-menu', createMenu);
  $('section').on('click', '.add-category', createCategory);
  $('section').on('click', '.delete-category', deleteCategory);
  $('section').on('click', '.add-menu-item', createMenuItem);
  $('section').on('click', '.delete-item', deleteMenuItem);
});
