import { endpoints } from "../constants";
import { postAsync } from "@/request";

export const UserService = {
  async changePassword(data) {
    return await postAsync(endpoints.changePassword, data);
  },
};
