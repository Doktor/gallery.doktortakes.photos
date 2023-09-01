import { getCsrfToken, getQueryString, sendRequest } from "../../utils";
import { endpoints } from "../../constants";

export const ManagePhotoService = {
  async getThumbnails(md5) {
    return await sendRequest(
      endpoints.managePhotoThumbnailList.replace(":md5", md5)
    );
  },

  async getRecentPhotos(page, size) {
    return await sendRequest(
      "/api/manage/photos/recent/" + getQueryString({ page, size })
    );
  },

  async createThumbnail(md5, options) {
    return await sendRequest(
      endpoints.managePhotoThumbnailList.replace(":md5", md5),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(options),
      }
    );
  },
};
