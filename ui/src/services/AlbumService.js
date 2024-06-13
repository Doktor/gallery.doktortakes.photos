import { getAsync, getQueryString, parseAlbumDetail } from "../utils";
import { endpoints } from "../constants";

export const AlbumService = {
  async getAllAlbums(full = false) {
    full = full ?? false;
    let query = full ? getQueryString({ full }) : "";

    let { content } = await getAsync(endpoints.albumList + query);
    let albums = content.albums;

    for (let album of albums) {
      album.pathSplit = album.path.split("/");
      album.tags?.sort();
    }

    return albums;
  },

  async getAlbum({ rawPath, code, getPhotos = true }) {
    let path = Array.isArray(rawPath) ? rawPath.join("/") : rawPath;
    let query = code ? getQueryString({ code }) : "";

    let { ok, content } = await getAsync(
      endpoints.albumDetail.replace(":path", path) + query,
    );

    if (!ok) {
      return { ok };
    }

    let { album, children } = content;

    if (!getPhotos) {
      return { ok, album };
    }

    ({ ok, content } = await getAsync(
      endpoints.albumPhotoList.replace(":path", path) + query,
    ));

    if (!ok) {
      return { ok };
    }

    let photos = content.photos;

    parseAlbumDetail(album, children);
    album.isLoaded = true;

    return { ok, album, photos };
  },
};
