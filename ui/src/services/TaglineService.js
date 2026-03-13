import { getAsync } from "@/request";

export const TaglineService = {
  async getTagline() {
    let { content } = await getAsync("/api/taglines/random/");
    return content;
  },
};
