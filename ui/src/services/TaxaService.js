import { sendRequest } from "@/utils";
import { endpoints } from "@/constants";

export const TaxaService = {
  async getTaxa() {
    let { content } = await sendRequest(endpoints.taxaList);
    return content;
  },
};
