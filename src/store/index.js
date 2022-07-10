import Vue from "vue";
import Vuex from "vuex";
import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";
import { production } from "@/constants";

Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    strict: !production,

    token: null,
    showNav: true,

    user: {},
    notifications: [],

    loading: 0,

    // Album
    album: {},
    photos: [],
    count: 0,
    selected: [],

    // Photo search
    searchResults: {
      page: 1,
      itemsPerPage: 10,
      photos: [],
      count: 0,
    },

    page: 1,
    loaded: [],

    // Settings
    photosPerPage: 30,
  },

  actions,
  getters,
  mutations,
});
