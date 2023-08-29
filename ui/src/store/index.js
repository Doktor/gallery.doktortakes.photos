import Vue from "vue";
import Vuex from "vuex";
import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";
import { production } from "../constants";

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    strict: !production,

    token: null,
    showNav: true,

    user: {},
    notifications: [],
    notificationId: 0,

    loading: 0,
  },

  actions,
  getters,
  mutations,
});
