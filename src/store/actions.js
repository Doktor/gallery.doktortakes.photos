import {endpoints, fields, getCsrfToken} from "./index.js";
import {router} from "../router/main.js";


function parseResponse(response) {
  return response.json().then(j => {
    return response.ok ? j : Promise.reject(j);
  });
}

function parseAlbumData(album) {
  let data = {};

  Object.entries(album).forEach(([key, value]) => {
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

  return data;
}


export const actions = {
  getUser(context) {
    if (Object.entries(context.state.user).length !== 0) {
      return Promise.resolve();
    }

    return fetch(endpoints.currentUser)
    .then(parseResponse)
    .then(j => context.commit('setUser', j))
    .catch(console.log);
  },

  getUserAlbums(context) {
    context.commit('setLoading', true);

    fetch(endpoints.currentUserAlbums)
    .then(parseResponse)
    .then(j => {
      context.commit('setLoading', false);
      context.commit('setAlbums', j.albums);
      context.commit('setPage', {page: 1, mutation: 'setAlbumPage'});
    })
    .catch(console.log);
  },

  changePassword(context, data) {
    fetch(endpoints.changePassword, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
    .then(parseResponse)
    .then(j => {
      flash(j.message);

      setTimeout(() => router.push({
        name: 'user',
        params: {
          slug: context.state.user.name
        },
      }), 1000);
    })
    .catch(j => j.errors.forEach(flash));
  },

  getAlbums(context) {
    context.commit('setLoading', true);

    fetch(endpoints.albumList)
    .then(parseResponse)
    .then(j => context.commit('setAlbums', j.albums))
    .then(() => {
      context.commit('setLoading', false);
      context.commit('setPage', {page: 1, mutation: 'setAlbumPage'});
    })
    .catch(console.log);
  },

  getAlbum(context, {path, setDocumentTitle, md5 = null}) {
    context.commit('setLoading', true);

    Promise.all([
      // Album data
      fetch(endpoints.albumDetail.replace(":path", path))
      .then(parseResponse)
      .then(j => context.commit('setAlbum', j))
      .catch(console.log),

      // Album photos
      fetch(endpoints.albumPhotoList.replace(":path", path))
      .then(parseResponse)
      .then(j => context.commit('setPhotos', j.photos))
      .catch(console.log),
    ])
    .then(() => {
      if (md5 !== null) {
        context.commit('setPhotoInitial', md5);
      } else {
        context.commit(setDocumentTitle);
      }
      context.commit('setLoading', false);
      context.commit('setPage', {page: 1, mutation: 'setPhotoPage'});
    })
    .catch(console.log);
  },

  getTags(context) {
    context.commit('setLoading', true);

    fetch(endpoints.tagList)
    .then(parseResponse)
    .then(j => {
      context.commit('setLoading', false);
      context.commit('setTags', j.tags);
    })
    .catch(console.log);
  },

  getTag(context, slug) {
    context.commit('setLoading', true);

    fetch(endpoints.tagDetail.replace(":slug", slug))
    .then(parseResponse)
    .then(j => {
      context.commit('setLoading', false);
      context.commit('setTag', j.tag);
      context.commit('setAlbums', j.albums);
      context.commit('setPage', {page: 1, mutation: 'setAlbumPage'});
    })
    .catch(console.log);
  },

  searchPhotos(context, queryString) {
    fetch(endpoints.searchPhotos + queryString)
    .then(parseResponse)
    .then(j => {
      context.commit('setSearchResults', j.photos);
      context.commit('setSearchResultsCount', j.count);
      context.commit('setPage', {page: j.page, mutation: 'setPhotoPage'});
    })
    .catch(console.log);
  },

  deleteAlbum() {
    fetch(endpoints.replace(":path", context.state.album.path), {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
    })
    .then(parseResponse)
    .then((j) => {
      flash("Album deleted successfully. Redirecting...");
      setTimeout(() => router.push({name: 'index'}), 1500);
    })
    .catch(console.log);
  },

  deleteSelected(context) {
    let photos = [];

    for (let photo of context.state.selected) {
      photos.push(photo.md5);
    }

    fetch(endpoints.albumPhotoList.replace(":path", context.state.album.path), {
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

  createAlbum(context) {
    let data = parseAlbumData(context.state.album);

    fetch(endpoints.albumList, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
    .then(parseResponse)
    .then(j => {
      let n = flash("Album created successfully. Redirecting...");
      setTimeout(
        () => router.push({name: 'editAlbum', params: {path: j.path}}),
        1500);
      setTimeout(() => n.remove(), 2500);
    })
    .catch(j => {
      for (let [field, errors] of Object.entries(j)) {
        for (let error of errors) {
          flash("{0}: {1}".format(field, error));
        }
      }
    });
  },

  saveAlbum(context) {
    let data = parseAlbumData(context.state.album);

    fetch(endpoints.albumDetail.replace(":path", context.state.album.path), {
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
      context.commit('updateDocumentTitleForEditor');
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

  setAlbumCover(context) {
    if (context.state.selected.length !== 1) {
      return;
    }

    let photo = context.state.selected[0];
    let current = context.state.album.cover;

    if (current !== null && photo.md5 === current.md5) {
      return;
    }

    let notification = flash("Setting cover image.");

    fetch(endpoints.albumDetail.replace(":path", context.state.album.path), {
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
