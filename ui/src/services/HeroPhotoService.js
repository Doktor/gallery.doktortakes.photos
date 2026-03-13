import { getAsync } from "@/request";

export const HeroPhotoService = {
  async list() {
    let { content } = await getAsync("/api/heroPhotos/");
    return content;
  },
};
