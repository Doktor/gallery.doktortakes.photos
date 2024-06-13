import { getAsync } from "../utils";
import { endpoints } from "../constants";

export const HeroPhotoService = {
  async list() {
    let { content } = await getAsync(endpoints.heroPhotoList);
    return content;
  },
};
