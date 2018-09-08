let $ = document.getElementById.bind(document);

const flashContainer = $('flash');

const form = $('album-form');

const api = $('api');
const API_ALBUM = api.dataset.apiAlbum;


function create_album() {
  let data = parse_form(form);

  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (request.readyState !== 4) {
      return;
    }

    let response = JSON.parse(request.responseText);

    if (request.status !== 200) {
      flash(response.error);
    } else {
      flash(response.message);

      setTimeout(function() {
        window.location.href = response.redirect_url;
      }, 2000);
    }
  };

  request.open('POST', API_ALBUM, true);
  request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  request.setRequestHeader("X-CSRFToken", get_cookie("csrftoken"));
  request.send(JSON.stringify(data));
}

$('album-form-save').addEventListener('click', create_album);
