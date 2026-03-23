import {
  getQueryString,
  parseAlbumDetail,
  prepareAlbumForRequest,
  parseAlbumResponse,
} from "@/utils";
import { store } from "@/store";
import { router } from "@/router";
import {
  deleteAsync,
  getAsync,
  patchAsync,
  postAsync,
  putAsync,
} from "@/request";

export const ManageAlbumService = {
  async createAlbum(album) {
    let data = prepareAlbumForRequest(album);

    let { ok, content } = await postAsync("/api/manage/albums/", data);

    if (!ok) {
      for (let [field, errors] of Object.entries(content)) {
        for (let error of errors) {
          store.commit("addNotification", {
            message: "{0}: {1}".format(field, error),
            status: "error",
          });
        }
      }

      return;
    }

    let path = content.path;

    if (!path) {
      store.commit("addNotification", {
        message: "An unknown API error occurred when creating the album.",
        status: "error",
      });
      return;
    }

    store.commit("addTimedNotification", {
      message: "Album created successfully. Redirecting...",
      status: "success",
      hideAfter: 2500,
    });

    setTimeout(
      () => router.push({ name: "editAlbum", params: { path: path } }),
      1500,
    );
  },

  async saveAlbum(album) {
    let data = prepareAlbumForRequest(album);

    let { ok, status, content } = await putAsync(
      `/api/manage/albums/${album.path}/`,
      data,
    );

    if (!ok) {
      if (status === 403) {
        store.commit("addNotification", {
          message: content.detail,
          status: "error",
        });
        return;
      }

      for (let [field, errors] of Object.entries(content)) {
        for (let error of errors) {
          store.commit("addNotification", {
            message: "{0}: {1}".format(field, error),
            status: "error",
          });
        }
      }
      return;
    }

    store.commit("addNotification", {
      message: "Album saved successfully.",
      status: "success",
    });

    let children;
    ({ album, children } = content);

    parseAlbumResponse(album, children);
    return album;
  },

  async setAlbumCover(album, photoHash) {
    let id = store.commit("addNotification", {
      message: "Setting cover photo.",
      status: "default",
    });

    let { ok, content } = await patchAsync(
      `/api/manage/albums/${album.path}/`,
      { cover: photoHash },
    );

    if (!ok) {
      store.commit("addNotification", {
        message: "An error occurred when setting the cover photo.",
        status: "error",
      });
      return;
    }

    store.commit("removeNotification", id);
    store.commit("addNotification", {
      message: "Cover photo set successfully.",
      status: "success",
    });

    let children;
    ({ album, children } = content);

    parseAlbumResponse(album, children);
    return album;
  },

  async deleteAlbum(path) {
    let { ok } = await deleteAsync(`/api/manage/albums/${path}/`);

    if (ok) {
      store.commit("addNotification", {
        message: "Album deleted successfully. Redirecting...",
        status: "success",
      });
      setTimeout(() => router.push({ name: "manage" }), 1500);
    }
  },

  async listAllPhotos(path) {
    return await getAsync(
      `/api/manage/albums/${path}/photos/` +
        getQueryString({ recursive: true }),
    );
  },

  async deletePhotos(path, photoHashes) {
    return await deleteAsync(`/api/manage/albums/${path}/photos/`, {
      photos: photoHashes,
    });
  },
};
