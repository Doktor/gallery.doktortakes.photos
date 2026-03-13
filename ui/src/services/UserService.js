import { getAsync, postAsync } from "@/request";

export const UserService = {
  async changePassword(data) {
    return await postAsync("/api/me/password/", data);
  },

  async ensureCsrfToken() {
    await getAsync("/api/csrf/");
  },

  async authenticate(username, password) {
    return await postAsync("/api/authenticate/", { username, password });
  },

  async getUser() {
    let { content } = await getAsync("/api/me/");
    return content;
  },
};
