import { sendRequest } from "@/utils";
import { endpoints } from "@/constants";

export const TaglineService = {
  async getTagline() {
    let { content } = await sendRequest(endpoints.randomTagline);
    return content;
  },
};
