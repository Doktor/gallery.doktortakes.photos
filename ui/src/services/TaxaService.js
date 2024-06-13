import { endpoints } from "@/constants";
import { getAsync } from "@/request";

export const TaxaService = {
  async getTaxa() {
    let { content } = await getAsync(endpoints.taxaList);
    return content;
  },

  async getSpecies() {
    let { content } = await getAsync("/api/taxa/species/");
    return content;
  },
};
