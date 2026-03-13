import { getAsync } from "@/request";

export const ManageLicenseService = {
  async listLicenses() {
    let { content } = await getAsync("/api/manage/licenses/");

    return content;
  },
};
