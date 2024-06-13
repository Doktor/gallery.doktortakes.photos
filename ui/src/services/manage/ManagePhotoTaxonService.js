import { deleteAsync, postAsync, putAsync } from "@/request";

export const ManagePhotoTaxonService = {
  async create(md5, taxon) {
    return await postAsync(`/api/manage/photos/${md5}/taxa/`, taxon);
  },

  async update(md5, catalogId, taxon) {
    return await putAsync(
      `/api/manage/photos/${md5}/taxa/${catalogId}/`,
      taxon,
    );
  },

  async delete(md5, catalogId) {
    return await deleteAsync(`/api/manage/photos/${md5}/taxa/${catalogId}/`);
  },
};
