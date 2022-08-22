import {sendRequest} from "@/utils";
import {endpoints} from "@/constants";

export const HeroPhotoService = {
  async list() {
    let { content } = await sendRequest(endpoints.heroPhotoList);
    return content;
  },
}