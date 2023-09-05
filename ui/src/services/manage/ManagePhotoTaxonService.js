import { getCsrfToken, sendRequest } from "@/utils";

export const ManagePhotoTaxonService = {
  async create(md5, taxon) {
    return await sendRequest(`/api/manage/photos/${md5}/taxa/`, {
      body: JSON.stringify(taxon),
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": getCsrfToken(),
      },
    });
  },

  async update(md5, catalogId, taxon) {
    return await sendRequest(`/api/manage/photos/${md5}/taxa/${catalogId}/`, {
      body: JSON.stringify(taxon),
      method: "PUT",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": getCsrfToken(),
      },
    });
  },

  async delete(md5, catalogId) {
    return await sendRequest(`/api/manage/photos/${md5}/taxa/${catalogId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRFToken": getCsrfToken(),
      },
    });
  },
};
