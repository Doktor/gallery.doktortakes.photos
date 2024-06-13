import { getAsync, getQueryString, postAsync } from "@/utils";
import { endpoints } from "@/constants";

export const ManagePhotoService = {
  async getThumbnails(md5) {
    return await getAsync(
      endpoints.managePhotoThumbnailList.replace(":md5", md5),
    );
  },

  async getRecentPhotos(page, size) {
    return await getAsync(
      "/api/manage/photos/recent/" + getQueryString({ page, size }),
    );
  },

  async createThumbnail(md5, data) {
    return await postAsync(
      endpoints.managePhotoThumbnailList.replace(":md5", md5),
      data,
    );
  },
};
