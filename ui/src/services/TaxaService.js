import { getAsync } from "@/request";

export const TaxaService = {
  async getTaxa() {
    let { content } = await getAsync("/api/taxa/");
    return content;
  },

  async getSpecies() {
    let { content } = await getAsync("/api/taxa/species/");
    return content;
  },
};
