import { getAsync } from "@/request";

export const PhotoService = {
  async get(md5) {
    return await getAsync(`/api/photos/${md5}/`);
  },

  async search(query) {
    let { content } = await getAsync("/api/photos/search/" + query);
    return content;
  },
};
