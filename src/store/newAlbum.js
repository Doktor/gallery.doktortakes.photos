import Vue from 'vue';
import Vuex from "vuex";
import {actions} from "../store/editAlbum/actions.js";
import {getters} from "../store/editAlbum/getters.js";
import {mutations} from "../store/editAlbum/mutations.js";

Vue.config.productionTip = process.env.NODE_ENV !== 'production';
Vue.use(Vuex);

export const store = new Vuex.Store({
  state: {
    album: {
      name: '',
      place: '',
      location: '',
      description: '',
      start: null,
      end: null,
      access_level: 0,
      access_code: '',
      users: '',
      groups: '',
      tags: '',
      parent: '',
    },
  },

  actions: actions,
  getters: getters,
  mutations: mutations,
});
