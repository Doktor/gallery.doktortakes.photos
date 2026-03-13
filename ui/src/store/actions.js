import { getAsync, postAsync } from "@/request";

export const actions = {
  async ensureCsrfToken(context) {
    await getAsync("/api/csrf/");
  },

  async authenticate(context, { username, password }) {
    return await postAsync("/api/authenticate/", { username, password });
  },

  async getUser(context) {
    let { content } = await getAsync("/api/me/");
    context.commit("setUser", content);
  },
};
