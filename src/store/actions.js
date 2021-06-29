import {endpoints, fields, getCsrfToken, getQueryString} from "./index.js";
import {router} from "../router/main.js";
import {store} from "@/store/index";


function addAuthorizationHeader(options) {
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
}


async function sendRequest(url, options = {}) {
  addAuthorizationHeader(options);

  try {
    let response = await fetch(url, options);
    return { ok: response.ok, status: response.status, content: await response.json() }
  } catch (error) {
    console.error(error);
  }
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
    await sendRequest(endpoints.csrf);
  },

  async authenticate(context, {username, password}) {
    return await sendRequest(endpoints.authenticate, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({username, password}),
    });
  },

  async getUsers(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.userList);
    let users = content.users.sort((a, b) => a.id - b.id);

    context.commit('setUsers', users);
    context.commit('setLoading', false);
  },

  async getUser(context) {
    let options = {};
    let token = context.state.token;

    if (token !== null) {
      options.headers = {'Authorization': `Token ${token}`};
    }

    let {content} = await sendRequest(endpoints.currentUser, options);
    context.commit('setUser', content);
  },

  async getGroups(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.groupList);
    let groups = content.groups.sort((a, b) => a.id - b.id);

    context.commit('setGroups', groups);
    context.commit('setLoading', false);
  },

  async changePassword(context, data) {
    let {ok, content} = await sendRequest(endpoints.changePassword, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (ok) {
      context.commit('addNotification', content.message);

      setTimeout(() => router.push({
        name: 'user',
        params: {
          slug: context.state.user.name
        },
      }), 1000);

      return;
    }

    content.errors.forEach((error) => {
      context.commit('addNotification', error);
    });
  },

  async getAllAlbums(context) {
    if (context.state.allAlbums.length > 0) {
      return Promise.resolve();
    }

    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.albumList);
    context.commit('setAllAlbums', content.albums);
    context.commit('setLoading', false);
  },

  async getAlbum(context, {rawPath, code}) {
    context.commit('setLoading', true);

    let path = Array.isArray(rawPath) ? rawPath.join('/') : rawPath;

    if (code) {
      return await context.dispatch('getAlbumWithAccessCode', {path, code})
    }

    if (context.state.albumPhotosCache.hasOwnProperty(path)) {
      await context.dispatch('getAllAlbums');

      context.commit('setPhotos', context.state.albumPhotosCache[path]);
      context.commit('setAlbumByPath', path);
      context.commit('setLoading', false);
      return;
    }

    await Promise.all([
      (async () => await context.dispatch('getAllAlbums'))(),
      (async () => {
        let {content} = await sendRequest(endpoints.albumPhotoList.replace(":path", path));

        context.commit('setPhotos', content.photos);
        context.commit('updateAlbumPhotosCache', {path: path, photos: content.photos});
      })(),
    ]);

    context.commit('setAlbumByPath', path);
    context.commit('setLoading', false);
    return Promise.resolve();
  },

  async getAlbumWithAccessCode(context, {path, code}) {
    let qs = getQueryString({code});

    await Promise.all([
      (async () => {
        let {content} = await sendRequest(endpoints.albumDetail.replace(":path", path) + qs);
        context.commit('setAlbum', content);
      })(),
      (async () => {
        let {content} = await sendRequest(endpoints.albumPhotoList.replace(":path", path) + qs);
        context.commit('setPhotos', content.photos);
      })(),
    ]);

    context.commit('setLoading', false);
  },

  async getTags(context) {
    if (context.state.tags.length > 0) {
      return Promise.resolve();
    }

    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.tagList);
    context.commit('setTags', content.tags);
    context.commit('setLoading', false);
  },

  async getFeaturedPhotos(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.featuredPhotos);
    let photos = content.photos;

    photos.forEach((photo, index) => {
      photo.index = index;
    });

    context.commit('setLoading', false);
    context.commit('setPhotos', photos);
    context.commit('setPhoto', {index: 0, history: false});
  },

  async searchPhotos(context, queryString) {
    let {content} = await sendRequest(endpoints.searchPhotos + queryString);
    context.commit('setSearchResults', content.photos);
    context.commit('setSearchResultsCount', content.count);
    context.commit('setPhotoPage', content.page);
  },

  async deleteAlbum(context) {
    let {ok} = await sendRequest(endpoints.replace(":path", context.state.album.path), {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (ok) {
      context.commit('addNotification', "Album deleted successfully. Redirecting...");
      setTimeout(() => router.push({name: 'editorIndex'}), 1500);
    }
  },

  async deleteSelected(context) {
    let photos = [];

    for (let photo of context.state.selected) {
      photos.push(photo.md5);
    }

    let {ok} = await sendRequest(endpoints.albumPhotoList.replace(":path", context.state.album.path), {
      method: 'DELETE',
      body: JSON.stringify({
        'photos': photos,
      }),
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (ok) {
      for (let photo of [...context.state.selected]) {
        photos.remove(photo);
        context.state.selected.remove(photo);
      }
    }
  },

  async createAlbum(context) {
    let data = parseAlbumForAPI(context.state.album);

    let {ok, content} = await sendRequest(endpoints.albumList, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (!ok) {
      for (let [field, errors] of Object.entries(content)) {
        for (let error of errors) {
          context.commit('addNotification', "{0}: {1}".format(field, error));
        }
      }

      return;
    }

    let path = content.path;

    if (!path) {
      context.commit('addNotification', "An unknown API error occurred when creating the album.");
      return;
    }

    context.commit('addAlbum', content);
    context.commit('updateAlbumPhotosCache', {path: content.path, photos: []});

    context.commit('addTimedNotification', {
      message: "Album created successfully. Redirecting...",
      hideAfter: 2500,
    });

    setTimeout(
      () => router.push({name: 'editAlbum', params: {path: path}}),
      1500);
  },

  async saveAlbum(context) {
    let data = parseAlbumForAPI(context.state.album);

    let {ok, status, content} = await sendRequest(endpoints.albumDetail.replace(":path", context.state.album.path), {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (!ok) {
      if (status === 403) {
        context.commit('addNotification', content.detail);
        return;
      }

      for (let [field, errors] of Object.entries(content)) {
        for (let error of errors) {
          context.commit('addNotification', "{0}: {1}".format(field, error));
        }
      }
      return;
    }

    context.commit('setAlbum', content);
    context.commit('updateDocumentTitleForEditAlbum');
    context.commit('addNotification', "Album saved successfully.");
  },

  async setAlbumCover(context) {
    if (context.state.selected.length !== 1) {
      return;
    }

    let photo = context.state.selected[0];
    let current = context.state.album.cover;

    if (current !== null && photo.md5 === current.md5) {
      return;
    }

    context.commit('addNotification', "Setting cover image.");

    let {content} = await sendRequest(endpoints.albumDetail.replace(":path", context.state.album.path), {
      method: 'PATCH',
      body: JSON.stringify({'cover': photo.md5}),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    context.commit('setAlbumField', {
      key: 'cover',
      value: content,
    });
    context.commit('removeNotification', "Setting cover image.");
    context.commit('addNotification', "Cover image set successfully.");
  },

  async getRecent(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.recent);
    context.commit('setAlbums', content.recent_albums);
    context.commit('setPage', {page: 1, mutation: 'setAlbumPage'});
    context.commit('setGitStatus', content.git_status);
    context.commit('setLoading', false);
  }
};
