import {getField} from "vuex-map-fields";


export const getters = {
  getField,

  isAuthenticated(state) {
    return state.token !== null;
  },

  getAccessCode(state) {
    return state.album.access_code;
  },

  albumPages(state) {
    return Math.ceil(state.results.length / state.albumsPerPage);
  },

  photoPages(state) {
    return Math.ceil(state.photos.length / state.photosPerPage);
  },
};
