import { getQueryString } from "@/utils";
import { getAsync, patchAsync, postAsync } from "@/request";

export const ManagePhotoService = {
  async getThumbnails(md5) {
    return await getAsync(
      `/api/manage/photos/${md5}/thumbnails/`,
    );
  },

  async getRecentPhotos(page, size) {
    return await getAsync(
      "/api/manage/photos/recent/" + getQueryString({ page, size }),
    );
  },

  async createThumbnail(md5, data) {
    return await postAsync(
      `/api/manage/photos/${md5}/thumbnails/`,
      data,
    );
  },

  async updatePhoto(md5, data) {
    return await patchAsync(`/api/manage/photos/${md5}/`, data);
  },
};
