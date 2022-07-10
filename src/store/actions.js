import { endpoints, getCsrfToken } from "./index.js";
import { router } from "@/router/main.js";
import { sendRequest } from "@/store/utils";

export const actions = {
  async ensureCsrfToken(context) {
    await sendRequest(endpoints.csrf);
  },

  async authenticate(context, { username, password }) {
    return await sendRequest(endpoints.authenticate, {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": getCsrfToken(),
      },
      body: JSON.stringify({ username, password }),
    });
  },

  async getUser(context) {
    let options = {};
    let token = context.state.token;

    if (token !== null) {
      options.headers = { Authorization: `Token ${token}` };
    }

    let { content } = await sendRequest(endpoints.currentUser, options);
    context.commit("setUser", content);
  },

  async changePassword(context, data) {
    let { ok, content } = await sendRequest(endpoints.changePassword, {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCsrfToken(),
      },
    });

    if (ok) {
      context.commit("addNotification", content.message);

      setTimeout(
        () =>
          router.push({
            name: "user",
            params: {
              slug: context.state.user.name,
            },
          }),
        1000
      );

      return;
    }

    content.errors.forEach((error) => {
      context.commit("addNotification", error);
    });
  },

  async searchPhotos(context, queryString) {
    let { content } = await sendRequest(endpoints.searchPhotos + queryString);
    context.commit("setSearchResults", content.photos);
    context.commit("setSearchResultsCount", content.count);
  },

  async getRecent(context) {
    context.commit("setLoading", true);

    let { content } = await sendRequest(endpoints.recent);
    context.commit("setLoading", false);
  },

  async getHeroPhotos(context) {
    let { content } = await sendRequest(endpoints.heroPhotoList);
    return content;
  },
};
