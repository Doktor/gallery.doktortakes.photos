import { getQueryString, sendRequest } from "@/utils";

export const TaxonPhotoService = {
  async get(catalogId, recursive = false) {
    return await sendRequest(
      `/api/taxa/${catalogId}/photos/` + getQueryString({ recursive }),
    );
  },
};
