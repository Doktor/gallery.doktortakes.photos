import {sendRequest} from "@/store/utils";
import {endpoints} from "@/store";

export const TaglineService = {
  async getTagline() {
    let {content} = await sendRequest(endpoints.randomTagline);
    return content;
  },
};