import {endpoints, fields, getCsrfToken, getQueryString} from "./index.js";
import {router} from "../router/main.js";
import {store} from "@/store/index";


async function parseResponse(response) {
  let j = await response.json();
  return response.ok ? j : Promise.reject(j);
}


async function sendRequest(url, options = {}) {
  if (store.state.token !== null) {
    let header = `Token ${store.state.token}`;

    if (options.hasOwnProperty("headers")) {
      options.headers['Authorization'] = header
    } else {
      options.headers = {
        'Authorization': header,
      }
    }
  }

  let response = await fetch(url, options);
  let json = await response.json();
  return response.ok ? json : Promise.reject(json);
}


function parseAlbumForAPI(album) {
  let data = {};

  Object.entries(album).forEach(([key, value]) => {
    // Don't send readonly fields
    if (fields.readonly.includes(key)) {
    }
    // Everything else
    else {
      data[key] = value;
    }
  });

  return data;
}


export const actions = {
  async ensureCsrfToken(context) {
    await fetch(endpoints.csrf);
  },

  async authenticate(context, {username, password}) {
    let response = await fetch(endpoints.authenticate, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({username, password}),
    });

    if (response.ok || response.status === 400) {
      return {ok: response.ok, content: await response.json()};
    }

    return Promise.reject(response);
  },

  async getUsers(context) {
    context.commit('setLoading', true);

    let response = await sendRequest(endpoints.userList);
    let users = response.users.sort((a, b) => a.id - b.id);

    context.commit('setUsers', users);
    context.commit('setLoading', false);
  },

  async getUser(context) {
    let options = {};
    let token = context.state.token;

    if (token !== null) {
      options.headers = {'Authorization': `Token ${token}`};
    }

    return await fetch(endpoints.currentUser, options)
    .then(parseResponse)
    .then(j => context.commit('setUser', j))
    .catch(console.log);
  },

  async getGroups(context) {
    context.commit('setLoading', true);

    let response = await sendRequest(endpoints.groupList);
    let groups = response.groups.sort((a, b) => a.id - b.id);

    context.commit('setGroups', groups);
    context.commit('setLoading', false);
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
      context.commit('addNotification', j.message);

      setTimeout(() => router.push({
        name: 'user',
        params: {
          slug: context.state.user.name
        },
      }), 1000);
    })
    .catch(j => {
      j.errors.forEach((err) => {
        context.commit('addNotification', err)
      });
    });
  },

  getAllAlbums(context) {
    if (context.state.allAlbums.length > 0) {
      return Promise.resolve();
    }

    context.commit('setLoading', true);

    return fetch(endpoints.albumList)
    .then(parseResponse)
    .then(j => {
      context.commit('setAllAlbums', j.albums);
      context.commit('setLoading', false);
    })
    .catch(console.log);
  },

  getAlbum(context, {rawPath, code}) {
    context.commit('setLoading', true);

    let path = Array.isArray(rawPath) ? rawPath.join('/') : rawPath;

    if (code) {
      return this.dispatch('getAlbumWithAccessCode', {path, code})
    }

    if (context.state.albumPhotosCache.hasOwnProperty(path)) {
      return context.dispatch('getAllAlbums').then(() => {
        context.commit('setPhotos', context.state.albumPhotosCache[path]);

        context.commit('setAlbumByPath', path);
        context.commit('setLoading', false);
      });
    } else {
      return Promise.all([
        context.dispatch('getAllAlbums'),

        fetch(endpoints.albumPhotoList.replace(":path", path))
        .then(parseResponse)
        .then(j => {
          context.commit('setPhotos', j.photos);
          context.commit('updateAlbumPhotosCache', {path: path, photos: j.photos});
        })
        .catch(console.log)
      ]).then(() => {
        context.commit('setAlbumByPath', path);
        context.commit('setLoading', false);
      });
    }
  },

  getAlbumWithAccessCode(context, {path, code}) {
    let qs = getQueryString({code});

    return Promise.all([
      fetch(endpoints.albumDetail.replace(":path", path) + qs)
      .then(parseResponse)
      .then(j => {
        context.commit('setAlbum', j);
      })
      .catch(console.log),

      fetch(endpoints.albumPhotoList.replace(":path", path) + qs)
      .then(parseResponse)
      .then(j => {
        context.commit('setPhotos', j.photos);
      })
      .catch(console.log),
    ]).then(() => {
      context.commit('setLoading', false);
    });
  },

  getTags(context) {
    if (context.state.tags.length > 0) {
      return Promise.resolve();
    }

    context.commit('setLoading', true);

    return fetch(endpoints.tagList)
    .then(parseResponse)
    .then(j => {
      context.commit('setLoading', false);
      context.commit('setTags', j.tags);
    })
    .catch(console.log);
  },

  getFeaturedPhotos(context) {
    context.commit('setLoading', true);

    fetch(endpoints.featuredPhotos)
    .then(parseResponse)
    .then(j => {
      let photos = j.photos;

      photos.forEach((photo, index) => {
        photo.index = index;
      });

      context.commit('setLoading', false);
      context.commit('setPhotos', photos);
      context.commit('setPhoto', {index: 0, history: false});
    })
    .catch(console.log);
  },

  searchPhotos(context, queryString) {
    fetch(endpoints.searchPhotos + queryString)
    .then(parseResponse)
    .then(j => {
      context.commit('setSearchResults', j.photos);
      context.commit('setSearchResultsCount', j.count);
      context.commit('setPhotoPage', j.page);
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
      context.commit('addNotification', "Album deleted successfully. Redirecting...");
      setTimeout(() => router.push({name: 'editorIndex'}), 1500);
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

  async createAlbum(context) {
    let data = parseAlbumForAPI(context.state.album);

    let rawResponse = await fetch(endpoints.albumList, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    let response;
    try {
      response = await parseResponse(rawResponse);
    } catch {
      for (let [field, errors] of Object.entries(j)) {
        for (let error of errors) {
          context.commit('addNotification', "{0}: {1}".format(field, error));
        }
      }
      return;
    }

    let path = response.path;

    if (!path) {
      context.commit('addNotification', "An unknown API error occurred when creating the album.");
      return;
    }

    context.commit('addAlbum', response);
    context.commit('updateAlbumPhotosCache', {path: response.path, photos: []});

    context.commit('addTimedNotification', {
      message: "Album created successfully. Redirecting...",
      hideAfter: 2500,
    });

    setTimeout(
      () => router.push({name: 'editAlbum', params: {path: path}}),
      1500);
  },

  saveAlbum(context) {
    let data = parseAlbumForAPI(context.state.album);

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
      context.commit('updateDocumentTitleForEditAlbum');
      context.commit('addNotification', "Album saved successfully.");
    })
    .catch(j => {
      for (let [field, errors] of Object.entries(j)) {
        for (let error of errors) {
          context.commit('addNotification', "{0}: {1}".format(field, error));
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

    context.commit('addNotification', "Setting cover image.");

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
      context.commit('removeNotification', "Setting cover image.");
      context.commit('addNotification', "Cover image set successfully.");
    })
    .catch(console.log);
  },

  getRecent(context) {
    context.commit('setLoading', true);

    fetch(endpoints.recent)
    .then(parseResponse)
    .then(j => {
      context.commit('setAlbums', j.recent_albums);
      context.commit('setPage', {page: 1, mutation: 'setAlbumPage'});
      context.commit('setGitStatus', j.git_status);
      context.commit('setLoading', false);
    })
    .catch(console.log);
  }
};
