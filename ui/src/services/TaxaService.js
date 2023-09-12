import { sendRequest } from "@/utils";
import { endpoints } from "@/constants";

export const TaxaService = {
  async getTaxa() {
    let { content } = await sendRequest(endpoints.taxaList);
    return content;
  },

  async getSpecies() {
    let { content } = await sendRequest("/api/taxa/species/");
    return content;
  },
};
