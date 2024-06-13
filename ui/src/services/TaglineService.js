import { getAsync } from "../utils";
import { endpoints } from "../constants";

export const TaglineService = {
  async getTagline() {
    let { content } = await getAsync(endpoints.randomTagline);
    return content;
  },
};
