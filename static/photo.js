const KEY_LEFT = 37;
const KEY_UP = 38;
const KEY_RIGHT = 39;
const KEY_DOWN = 40;

const urls = document.getElementById('navigation');

const previous_url = urls.dataset.urlPrevious;
const next_url = urls.dataset.urlNext;
const first_url = urls.dataset.urlFirst;
const last_url = urls.dataset.urlLast;

function navigate(url) {
  let request = new XMLHttpRequest();

  request.onreadystatechange = function() {
    if (!(request.readyState === 4 && request.status === 200)) {
      return;
    }

    let response = JSON.parse(request.responseText);

    let photo = document.getElementById('photo');
    let image = photo.children[0];

    photo.dataset.md5 = response.md5;
    image.src = response.image;
    window.history.pushState('', '', response.url);
  };

  request.open('GET', url, true);
  request.send();
}

function query_string(params) {
  let escape = encodeURIComponent;
  let query = Object.keys(params)
    .map(k => escape(k) + '=' + escape(params[k]))
    .join('&');

  return '?' + query;
}

document.onkeydown = function(e) {
  let photo = document.getElementById('photo');

  let query = query_string({
    'path': photo.dataset.path,
    'md5': photo.dataset.md5,
  });

  switch (e.keyCode) {
    case KEY_LEFT:
      return navigate(previous_url + query);
    case KEY_RIGHT:
      return navigate(next_url + query);
    case KEY_UP:
      return navigate(first_url + query);
    case KEY_DOWN:
      return navigate(last_url + query);
  }
};
