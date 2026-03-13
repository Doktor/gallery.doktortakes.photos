import { postAsync } from "@/request";

export const ManageTaxaService = {
  async importTaxon(catalogId) {
    return await postAsync("/api/manage/taxa/import/", { catalogId });
  },
};
