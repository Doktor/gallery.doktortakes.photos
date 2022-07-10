import { sendRequest } from "@/store/utils";
import { endpoints } from "@/store";

export const ManageUserService = {
  async listUsers() {
    let { content } = await sendRequest(endpoints.userList);
    return content.users.sort((a, b) => a.id - b.id);
  },

  async listGroups() {
    let { content } = await sendRequest(endpoints.groupList);
    return content.groups.sort((a, b) => a.id - b.id);
  },
};
