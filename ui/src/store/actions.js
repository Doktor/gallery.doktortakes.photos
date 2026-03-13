import { UserService } from "@/services/UserService";

export const actions = {
  async ensureCsrfToken(context) {
    await UserService.ensureCsrfToken();
  },

  async authenticate(context, { username, password }) {
    return await UserService.authenticate(username, password);
  },

  async getUser(context) {
    let content = await UserService.getUser();
    context.commit("setUser", content);
  },
};
