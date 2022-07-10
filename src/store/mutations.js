import Vue from "vue";
import { updateField } from "vuex-map-fields";
import { router } from "@/router/main.js";

export const titleTemplate = "{0} | Doktor Takes Photos";
export const editorTitleTemplate = "Editing {0} | Doktor Takes Photos";

export const mutations = {
  // vuex-map-fields
  updateField,

  setApiTokenFromLocalStorage(state) {
    state.token = localStorage.getItem("token");
  },

  setApiToken(state, token) {
    state.token = token;
    localStorage.setItem("token", token);
  },

  logOut(state) {
    state.token = null;
    localStorage.removeItem("token");

    state.user = { status: "anonymous" };
  },

  addNotification(state, message) {
    if (state.notifications.includes(message)) {
      return;
    }

    state.notifications.push(message);
  },

  addTimedNotification(state, { message, hideAfter = 0 }) {
    this.commit("addNotification", message);

    if (hideAfter > 0) {
      setTimeout(() => this.commit("removeNotification", message), hideAfter);
    }
  },

  removeNotification(state, message) {
    state.notifications.remove(message);
  },

  setUser(state, user) {
    state.user = user;
  },

  setSearchResults(state, photos) {
    state.searchResults.photos = photos;
  },

  clearSearchResults(state) {
    state.searchResults.photos = Array(state.searchResults.itemsPerPage).fill(
      {}
    );
  },

  setSearchResultsItemsPerPage(state, itemsPerPage) {
    state.searchResults.itemsPerPage = itemsPerPage;
  },

  setSearchResultsPage(state, page) {
    state.searchResults.page = page;
  },

  setSearchResultsCount(state, count) {
    state.searchResults.count = count;
  },

  setLoading(state, loading) {
    loading ? (state.loading += 1) : (state.loading -= 1);
  },

  setAlbumField(state, data) {
    Vue.set(state.album, data.key, data.value);
  },

  setPhotos(state, photos) {
    for (let [index, photo] of photos.entries()) {
      photo.index = index;
      photo.page = Math.floor(index / state.photosPerPage) + 1;
      photo.loaded = false;
    }

    state.photos = photos;
  },
};
