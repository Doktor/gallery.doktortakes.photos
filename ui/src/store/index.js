import { createStore } from "vuex";
import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";
import { production } from "../constants";

export const store = createStore({
  state: {
    strict: !production,

    token: null,
    showNavigation: true,
    breadcrumbs: [],

    user: {},
    notifications: [],
    notificationId: 0,

    loading: 0,
  },

  actions,
  getters,
  mutations,
});
