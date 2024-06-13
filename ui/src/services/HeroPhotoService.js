import { endpoints } from "../constants";
import { getAsync } from "@/request";

export const HeroPhotoService = {
  async list() {
    let { content } = await getAsync(endpoints.heroPhotoList);
    return content;
  },
};
