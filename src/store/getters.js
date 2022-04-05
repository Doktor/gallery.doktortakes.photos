import { getField } from "vuex-map-fields";

export const getters = {
  getField,

  isAuthenticated(state) {
    return state.token !== null;
  },
  isStaff(state) {
    return state.user.status === "staff" || state.user.status === "superuser";
  },

  getAccessCode(state) {
    return state.album.access_code;
  },
};
