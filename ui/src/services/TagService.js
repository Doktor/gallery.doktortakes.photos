import { getAsync } from "../utils";
import { endpoints } from "../constants";

export const TagService = {
  async getTags() {
    let { content } = await getAsync(endpoints.tagList);
    return content.tags;
  },

  async getTag(slug) {
    let tags = await this.getTags();
    return tags.find((tag) => tag.slug === slug);
  },
};
