import { parseAlbumForAPI, sendRequest } from "@/store/utils";
import { endpoints, getCsrfToken } from "@/store";
import { router } from "@/router/main";

export const actions = {
  async deleteAlbum(context) {
    let { ok } = await sendRequest(
      endpoints.replace(":path", context.rootState.album.path),
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "X-CSRFToken": getCsrfToken(),
        },
      }
    );

    if (ok) {
      context.commit(
        "addNotification",
        "Album deleted successfully. Redirecting..."
      );
      setTimeout(() => router.push({ name: "manage" }), 1500);
    }
  },

  async createAlbum(context, album) {
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
          context.commit("addNotification", "{0}: {1}".format(field, error));
        }
      }

      return;
    }

    let path = content.path;

    if (!path) {
      context.commit(
        "addNotification",
        "An unknown API error occurred when creating the album."
      );
      return;
    }

    context.commit("addTimedNotification", {
      message: "Album created successfully. Redirecting...",
      hideAfter: 2500,
    });

    setTimeout(
      () => router.push({ name: "editAlbum", params: { path: path } }),
      1500
    );
  },

  async saveAlbum(context, album) {
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
        context.commit("addNotification", content.detail);
        return;
      }

      for (let [field, errors] of Object.entries(content)) {
        for (let error of errors) {
          context.commit("addNotification", "{0}: {1}".format(field, error));
        }
      }
      return;
    }

    context.commit("addNotification", "Album saved successfully.");
  },
};
