let $ = document.getElementById.bind(document);

const form = $('album-form');

const api = $('api');
const API_ALBUM = api.dataset.apiAlbum;


$('album-form-save').addEventListener('click', () => {
  function onError(response) {
    flash(response.error);
  }

  function onSuccess(response) {
    flash(response.message);

    setTimeout(function() {
      window.location.href = response.redirect_url;
    }, 2000);
  }

  let data = parse_form(form);

  send_request('POST', API_ALBUM, onSuccess, onError, data, true);
});
