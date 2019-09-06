import {endpoints, fields, getCsrfToken} from "./index.js";


function parseResponse(response) {
  return response.json().then(j => {
    return response.ok ? j : Promise.reject(j);
  });
}


export const actions = {
  getData(context) {
    Promise.all([
      // Album data
      fetch(endpoints.album)
      .then(parseResponse)
      .then(j => context.commit('setAlbum', j))
      .catch(console.log),

      // Album photos
      fetch(endpoints.albumPhotos)
      .then(parseResponse)
      .then(j => context.commit('setPhotos', j.photos))
      .catch(console.log),

    ]).then(() => context.state.loading = false);
  },

  deleteAlbum() {
    fetch(endpoints.album, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
    })
    .then(parseResponse)
    .then((j) => {
      flash("Album deleted successfully. Redirecting...");
      setTimeout(() => window.location = j.redirect_to, 1500);
    })
    .catch(console.log);
  },

  deleteSelected(context) {
    let photos = [];

    for (let photo of context.state.selected) {
      photos.push(photo.md5);
    }

    fetch(endpoints.albumPhotos, {
      method: 'DELETE',
      body: JSON.stringify({
        'photos': photos,
      }),
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
    })
    .then(parseResponse)
    .then((j) => {
      for (let photo of [...context.state.selected]) {
        photos.remove(photo);
        context.state.selected.remove(photo);
      }
    })
    .catch(console.log);
  },

  saveAlbum(context) {
    let data = {};

    // Prepare data for sending
    Object.entries(context.state.album).forEach(([key, value]) => {
      // Don't send readonly fields
      if (fields.readonly.includes(key)) {
      }
      // Parse list fields
      else if (fields.list.includes(key)) {
        data[key] = value.split(',').filter(x => x.trim().length > 0);
      }
      // Everything else
      else {
        data[key] = value;
      }
    });

    fetch(endpoints.album, {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
    .then(parseResponse)
    .then(j => {
      context.commit('setAlbum', j);
      flash("Album saved successfully.");
    })
    .catch(j => {
      for (let [field, errors] of Object.entries(j)) {
        for (let error of errors) {
          flash("{0}: {1}".format(field, error));
        }
      }
    });
  },

  setCover(context) {
    if (context.state.selected.length !== 1) {
      return;
    }

    let photo = context.state.selected[0];
    let current = context.state.album.cover;

    if (current !== null && photo.md5 === current.md5) {
      return;
    }

    let notification = flash("Setting cover image.");

    fetch(endpoints.album, {
      method: 'PATCH',
      body: JSON.stringify({'cover': photo.md5}),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
    .then(parseResponse)
    .then(j => {
      context.commit('setAlbumField', {
        key: 'cover',
        value: j,
      });
      notification.remove();
      flash("Cover image set successfully.")
    })
    .catch(console.log);
  }
};
