import { endpoints } from "@/constants";

import { getAsync } from "@/request";

export const ManageLicenseService = {
  async listLicenses() {
    let { content } = await getAsync(endpoints.manageLicenseList);

    return content;
  },
};
