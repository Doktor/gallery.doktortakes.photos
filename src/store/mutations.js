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

  addNotification(state, { message, status = "note" }) {
    state.notificationId += 1;

    let notification = { id: state.notificationId, message, status };
    state.notifications.push(notification);

    return notification.id;
  },

  addTimedNotification(state, { message, status = "note", hideAfter = 0 }) {
    let id = this.commit("addNotification", { message, status });

    if (hideAfter > 0) {
      setTimeout(() => this.commit("removeNotification", id), hideAfter);
    }
  },

  removeNotification(state, id) {
    let index = state.notifications.findIndex((n) => n.id === id);
    state.notifications.splice(index, 1);
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
