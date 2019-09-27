import Vue from 'vue';
import Vuex from "vuex";
import {getField, updateField} from "vuex-map-fields";


Vue.config.productionTip = process.env.NODE_ENV !== 'production';
Vue.use(Vuex);


const api = document.getElementById('api');

export const endpoints = {
  albumList: api.dataset.apiAlbumList,
};

export const staticFiles = {
  coverPlaceholder: api.dataset.staticCoverPlaceholder,
};


function parseResponse(response) {
  return response.json().then(j => {
    return response.ok ? j : Promise.reject(j);
  });
}


const actions = {
  getAlbums(context) {
    fetch(endpoints.albumList)
    .then(parseResponse)
    .then(j => {
      context.commit('setAlbums', j.albums);
      context.state.loading = false;
      context.commit('changePage', 1);
    })
    .catch(console.log);
  },
};


const getters = {
  getField,

  itemsPerPage(state) {
    return state.settings.itemsPerPage;
  },

  pages(state) {
    return Math.ceil(state.results.length / state.settings.itemsPerPage);
  },
};


const mutations = {
  updateField,

  changePage(state, page) {
    state.page = page;

    state.results.filter((album) => !album.loaded).forEach((album, index) => {
      if (page === Math.floor(index / state.settings.itemsPerPage) + 1) {
        album.isLoaded = true;
      }
    });
  },

  filterAlbums(state) {
    let term = state.search;

    if (!term) {
      state.results = state.albums;
      return;
    }

    state.results = state.albums.filter(
      (album) => album.name.match(new RegExp(term, "i")));
    this.commit('changePage', 1);
  },

  setAlbums(state, albums) {
    albums.map((album) => album.isLoaded = false);

    state.albums = albums;
    state.results = state.albums;
  }
};


export const store = new Vuex.Store({
  state: {
    albums: [],
    results: [],
    loading: true,
    search: '',

    page: 1,
    pagesLoaded: [],

    settings: {
      itemsPerPage: 12,
    }
  },

  actions,
  getters,
  mutations,
});
