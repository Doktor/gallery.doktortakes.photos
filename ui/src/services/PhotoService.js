import { getAsync } from "@/request";

export const PhotoService = {
  async get(md5) {
    return await getAsync(`/api/photos/${md5}/`);
  },
};
