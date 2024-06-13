import { endpoints } from "../constants";
import { getAsync } from "@/request";

export const TaglineService = {
  async getTagline() {
    let { content } = await getAsync(endpoints.randomTagline);
    return content;
  },
};
