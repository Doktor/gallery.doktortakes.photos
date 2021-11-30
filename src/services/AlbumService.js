import {sendRequest} from "@/store/utils";
import {endpoints, getQueryString} from "@/store";

export const AlbumService = {
  async getAllAlbums() {
    let {content} = await sendRequest(endpoints.albumList);
    let albums = content.albums;

    for (let album of albums) {
      album.pathSplit = album.path.split('/');
      album.tags.sort();
    }

    return albums;
  },

  async getAlbum({rawPath, code}) {
    let path = Array.isArray(rawPath) ? rawPath.join('/') : rawPath;
    let query = code ? getQueryString({code}) : "";

    let {ok, content} = await sendRequest(endpoints.albumDetail.replace(":path", path) + query);

    if (!ok) {
      return {ok};
    }

    let album = content;

    ({ok, content} = await sendRequest(endpoints.albumPhotoList.replace(":path", path) + query));

    if (!ok) {
      return {ok};
    }

    let photos = content.photos;

    album.isLoaded = true;
    album.pathSplit = album.path.split('/');
    album.tags.sort();

    return {ok, album, photos};
  },
};
