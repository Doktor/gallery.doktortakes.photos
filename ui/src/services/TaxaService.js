import { getAsync } from "@/utils";
import { endpoints } from "@/constants";

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
