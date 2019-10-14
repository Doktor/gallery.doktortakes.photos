import {getField} from "vuex-map-fields";


export const getters = {
  getField,

  getAccessCode(state) {
    return state.album.access_code;
  },

  albumsPerPage(state) {
    return state.settings.albumsPerPage;
  },

  photosPerPage(state) {
    return state.settings.photosPerPage;
  },

  albumPages(state) {
    return Math.ceil(state.results.length / state.settings.albumsPerPage);
  },

  photoPages(state) {
    return Math.ceil(state.photos.length / state.settings.photosPerPage);
  },
};
