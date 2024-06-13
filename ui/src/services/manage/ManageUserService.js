import { endpoints } from "@/constants";
import { getAsync } from "@/request";

export const ManageUserService = {
  async listUsers() {
    let { content } = await getAsync(endpoints.userList);
    return content.users.sort((a, b) => a.id - b.id);
  },

  async listGroups() {
    let { content } = await getAsync(endpoints.groupList);
    return content.groups.sort((a, b) => a.id - b.id);
  },
};
