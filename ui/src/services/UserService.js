import { postAsync } from "@/request";

export const UserService = {
  async changePassword(data) {
    return await postAsync("/api/me/password/", data);
  },
};
