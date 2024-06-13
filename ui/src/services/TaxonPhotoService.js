import { getQueryString } from "@/utils";
import { getAsync } from "@/request";

export const TaxonPhotoService = {
  async get(catalogId, recursive = false) {
    return await getAsync(
      `/api/taxa/${catalogId}/photos/` + getQueryString({ recursive }),
    );
  },
};
