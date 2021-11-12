import { parseAlbumForAPI, sendRequest } from "@/store/utils";
import { endpoints, getCsrfToken } from "@/store";
import { router } from "@/router/main";


export const actions = {
  async deleteAlbum(context) {
    let {ok} = await sendRequest(endpoints.replace(":path", context.rootState.album.path), {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (ok) {
      context.commit('addNotification', "Album deleted successfully. Redirecting...");
      setTimeout(() => router.push({name: 'manage'}), 1500);
    }
  },

  async deleteSelected(context) {
    let photos = [];

    for (let photo of context.rootState.selected) {
      photos.push(photo.md5);
    }

    let {ok} = await sendRequest(endpoints.albumPhotoList.replace(":path", context.rootState.album.path), {
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
      for (let photo of [...context.rootState.selected]) {
        photos.remove(photo);
        context.rootState.selected.remove(photo);
      }
    }
  },

  async createAlbum(context) {
    let data = parseAlbumForAPI(context.rootState.album);

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

    context.commit('addTimedNotification', {
      message: "Album created successfully. Redirecting...",
      hideAfter: 2500,
    });

    setTimeout(
      () => router.push({name: 'editAlbum', params: {path: path}}),
      1500);
  },

  async saveAlbum(context) {
    let data = parseAlbumForAPI(context.rootState.album);

    let {ok, status, content} = await sendRequest(endpoints.albumDetail.replace(":path", context.rootState.album.path), {
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
    if (context.rootState.selected.length !== 1) {
      return;
    }

    let photo = context.rootState.selected[0];
    let current = context.rootState.album.cover;

    if (current !== null && photo.md5 === current.md5) {
      return;
    }

    context.commit('addNotification', "Setting cover image.");

    let {content} = await sendRequest(endpoints.albumDetail.replace(":path", context.rootState.album.path), {
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
};
