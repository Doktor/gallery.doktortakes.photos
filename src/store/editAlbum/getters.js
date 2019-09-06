import {getField} from "vuex-map-fields";


export const getters = {
  getField,

  getAccessCode(state) {
    return state.album.access_code;
  },

  itemsPerPage(state) {
    return state.settings.itemsPerPage;
  },

  pages(state) {
    return Math.ceil(state.photos.length / state.settings.itemsPerPage);
  },
};
