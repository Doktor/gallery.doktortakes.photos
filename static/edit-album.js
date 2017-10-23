function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function delete_photo(number, element) {
  var request = new XMLHttpRequest();

  request.onreadystatechange = function () {
    if (request.readyState === 4 && request.status === 200) {
      var response = JSON.parse(request.responseText);

      if (response.success) {
        element.parentNode.remove();
        update_total();
        update_counter();
      }
    }
  };

  var url = "{% url 'album' album.get_path %}" + number;
  request.open("DELETE", url, true);
  request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
  request.send();
}

Element.prototype.remove = function () {
  this.parentElement.removeChild(this);
};

var selected = [];
var photos = document.getElementsByClassName('photo');

var deleteButton = document.getElementById('delete-photos');
deleteButton.addEventListener('click', function () {
  for (var i = 0; i < selected.length; i++) {
    var number = selected[i].getAttribute('data-number');
    delete_photo(number, selected[i]);
  }
});

function update_total() {
  var total = document.getElementById('total');
  var photos = document.getElementsByClassName('photo');
  var count = photos.length;

  if (count === 1) {
    total.textContent = count + ' photo in album';
  } else {
    total.textContent = count + ' photos in album';
  }
}

function update_counter() {
  var counter = document.getElementById('counter');
  var selected = document.getElementsByClassName('selected');
  var count = selected.length;

  if (count === 1) {
    counter.textContent = count + ' photo selected';
  } else {
    counter.textContent = count + ' photos selected';
  }
}

function select_all() {
  for (var i = 0; i < photos.length; i++) {
    photos[i].classList.add('selected');
    selected.push(photos[i]);
  }
  update_counter();
}

function select_none() {
  for (var i = 0; i < photos.length; i++) {
    photos[i].classList.remove('selected');
  }
  selected = [];
  update_counter();
}

for (var i = 0; i < photos.length; i++) {
  var el = photos[i];

  el.addEventListener('click', function () {
    // Not selected
    if (!this.classList.contains('selected')) {
      this.classList.add('selected');
      selected.push(this);
    } else {
      // Selected
      this.classList.remove('selected');
      var index = selected.indexOf(this);
      if (index > -1) {
        selected.splice(index, 1);
      }
    }
    update_counter();
  });
}
