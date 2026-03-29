import { getQueryString, parseAlbumResponse } from "../utils";
import { getAsync } from "@/request";

export const AlbumService = {
  async getAllAlbums(userId = null, tagSlug = null) {
    let query = getQueryString({ userId, tag: tagSlug });

    let { content } = await getAsync("/api/albums/" + query);

    content.albums.forEach((album) => parseAlbumResponse(album, []));
    return content.albums;
  },

  async getExternalAlbums() {
    let { content } = await getAsync("/api/appearances/albums/");

    content.albums.forEach((album) => parseAlbumResponse(album, []));
    return content.albums;
  },

  async getAlbumsForUser(userId) {
    return await this.getAllAlbums(userId, null);
  },

  async getAlbumsForTag(tagSlug) {
    return await this.getAllAlbums(null, tagSlug);
  },

  async getFeaturedAlbums() {
    let { content } = await getAsync("/api/albums/featured/");
    let albums = content.albums.map((a) => ({
      ...a,
      parentName: a.parent_name,
      accessLevel: a.access_level,
    }));
    albums.sort((a, b) => new Date(b.start) - new Date(a.start));
    return albums;
  },

  async getAlbum({ rawPath, code, getPhotos = true }) {
    let path = Array.isArray(rawPath) ? rawPath.join("/") : rawPath;
    let query = code ? getQueryString({ code }) : "";

    let { ok, content } = await getAsync(`/api/albums/${path}/` + query);

    if (!ok) {
      return { ok };
    }

    let { album, children, photos } = content;

    if (!getPhotos) {
      return { ok, album };
    }

    parseAlbumResponse(album, children);
    album.isLoaded = true;

    return { ok, album, photos };
  },
};
