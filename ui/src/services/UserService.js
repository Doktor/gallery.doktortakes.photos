import { postAsync } from "../utils";
import { endpoints } from "../constants";

export const UserService = {
  async changePassword(data) {
    return await postAsync(endpoints.changePassword, data);
  },
};
