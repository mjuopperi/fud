
function showProgressIndicator(button) {
  button.addClass('loading').prop('disabled', true);
}

function hideProgressIndicator(button) {
  button.removeClass('loading').prop('disabled', false);
}

function showSuccesIndicator(form) {
  form.find('.success').show().delay(1000).fadeOut();
}

exports.showProgressIndicator = showProgressIndicator;
exports.hideProgressIndicator = hideProgressIndicator;
exports.showSuccesIndicator = showSuccesIndicator;