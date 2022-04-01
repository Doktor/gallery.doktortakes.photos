import { endpoints } from "@/store";
import { sendRequest } from "@/store/utils";

export const PhotoService = {
  async get(md5) {
    return await sendRequest(endpoints.photoDetail.replace(":md5", md5));
  },

  async getThumbnails(md5) {
    return await sendRequest(endpoints.thumbnailList.replace(":md5", md5));
  },
};
