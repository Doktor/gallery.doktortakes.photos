import { endpoints } from "../constants";
import { getAsync, postAsync } from "@/request";

export const actions = {
  async ensureCsrfToken(context) {
    await getAsync(endpoints.csrf);
  },

  async authenticate(context, { username, password }) {
    return await postAsync(endpoints.authenticate, { username, password });
  },

  async getUser(context) {
    let { content } = await getAsync(endpoints.currentUser);
    context.commit("setUser", content);
  },
};
