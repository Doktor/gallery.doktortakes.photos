import { getCsrfToken, parseAlbumForAPI, sendRequest } from "@/utils";
import { store } from "@/store";
import { router } from "@/router/main";
import { endpoints } from "@/constants";

export const ManageAlbumService = {
  async createAlbum(album) {
    let data = parseAlbumForAPI(album);

    let { ok, content } = await sendRequest(endpoints.albumList, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
    });

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
      1500
    );
  },

  async saveAlbum(album) {
    let data = parseAlbumForAPI(album);

    let { ok, status, content } = await sendRequest(
      endpoints.albumDetail.replace(":path", album.path),
      {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
      }
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
  },

  async deleteAlbum(path) {
    let { ok } = await sendRequest(
      endpoints.albumDetail.replace(":path", path),
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "X-CSRFToken": getCsrfToken(),
        },
      }
    );

    if (ok) {
      store.commit("addNotification", {
        message: "Album deleted successfully. Redirecting...",
        status: "success",
      });
      setTimeout(() => router.push({ name: "manage" }), 1500);
    }
  },
};
