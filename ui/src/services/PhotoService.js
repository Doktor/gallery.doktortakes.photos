import { endpoints } from "../constants";
import { getAsync } from "@/request";

export const PhotoService = {
  async get(md5) {
    return await getAsync(endpoints.photoDetail.replace(":md5", md5));
  },
};
