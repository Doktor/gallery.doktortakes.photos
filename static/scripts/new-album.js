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
      window.location.href = response.redirectUrl;
    }, 2000);
  }

  let data = parseForm(form);

  sendRequest('POST', API_ALBUM, onSuccess, onError, data, true);
});
