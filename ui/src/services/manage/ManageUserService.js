import { getAsync } from "@/request";

export const ManageUserService = {
  async listUsers() {
    let { content } = await getAsync("/api/manage/users/");
    return content.users.sort((a, b) => a.id - b.id);
  },

  async listGroups() {
    let { content } = await getAsync("/api/manage/groups/");
    return content.groups.sort((a, b) => a.id - b.id);
  },
};
