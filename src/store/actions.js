import { getCsrfToken, sendRequest } from "@/utils";
import { endpoints } from "@/constants";

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
