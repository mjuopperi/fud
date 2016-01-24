require('./_header');
var util = require('./_util');

function buildTemplate() {
  return _.template(
    $("script.template").html()
  );
}

function renderMenu(data) {
  const template = buildTemplate();
  $("section").html(template(data));
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
  getMenu();
}

$(function() {
  init();
});
