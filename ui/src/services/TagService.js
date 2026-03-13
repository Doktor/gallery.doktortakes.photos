import { getAsync } from "@/request";

export const TagService = {
  async getTags() {
    let { content } = await getAsync("/api/tags/");
    return content.tags;
  },

  async getTag(slug) {
    let tags = await this.getTags();
    return tags.find((tag) => tag.slug === slug);
  },
};
