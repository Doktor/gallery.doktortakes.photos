import { getAsync, getQueryString } from "@/utils";

export const TaxonPhotoService = {
  async get(catalogId, recursive = false) {
    return await getAsync(
      `/api/taxa/${catalogId}/photos/` + getQueryString({ recursive }),
    );
  },
};
