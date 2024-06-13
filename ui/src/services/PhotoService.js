import { getAsync } from "../utils";
import { endpoints } from "../constants";

export const PhotoService = {
  async get(md5) {
    return await getAsync(endpoints.photoDetail.replace(":md5", md5));
  },
};
