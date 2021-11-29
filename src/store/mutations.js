import Vue from "vue";
import {updateField} from "vuex-map-fields";
import {router} from "@/router/main.js";


const titleTemplate = "{0} | Doktor Takes Photos";
const editorTitleTemplate = "Editing {0} | Doktor Takes Photos";


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

    state.user = {status: "anonymous"};

    this.commit('setAllAlbums', []);
    this.commit('setAlbums', []);
  },

  addNotification(state, message) {
    if (state.notifications.includes(message)) {
      return;
    }

    state.notifications.push(message);
  },

  addTimedNotification(state, {message, hideAfter = 0}) {
    this.commit('addNotification', message);

    if (hideAfter > 0) {
      setTimeout(() => this.commit('removeNotification', message), hideAfter);
    }
  },

  removeNotification(state, message) {
    state.notifications.remove(message);
  },

  setUser(state, user) {
    state.user = user;
  },

  setPhotoPage(state, page) {
    state.page = page;
    state.loaded.push(page);
  },

  setSearchResults(state, photos) {
    state.searchResults.photos = photos;
  },

  clearSearchResults(state) {
    state.searchResults.photos = Array(state.searchResults.itemsPerPage).fill({});
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

  filterAlbums(state) {
    let term = state.search;

    if (!term) {
      state.results = state.albums;
      return;
    }

    state.results = state.albums.filter(
      (album) => album.name.match(new RegExp(term, "i")));
  },

  setAllAlbums(state, albums) {
    albums.map((album) => {
      album.isLoaded = false;
      album.pathSplit = album.path.split('/');
      album.tags.sort();
      return album;
    });

    albums.map((album) => {
      // Child albums are sent in this format: [{path: "..."}, {path: "..."}, ...]
      let childPaths = album.children.map((item) => item.path);
      album.children = [...albums.filter((album) => childPaths.includes(album.path))];
      return album;
    });

    state.allAlbums = albums;
    state.albums = albums;
    state.results = albums;
  },

  addAlbum(state, album) {
    state.allAlbums.push(album);
  },

  setAlbums(state, albums) {
    state.albums = albums;
    state.results = albums;
  },

  setAlbumsByTag(state, tag) {
    this.commit('setAlbums', state.allAlbums.filter((album) => album.tags.includes(tag)));
  },

  setAlbumsToTopLevelAlbums(state) {
    this.commit('setAlbums', state.allAlbums.filter((album) => album.parent === null));
  },

  setAlbumsToPrivateAlbums(state) {
    this.commit('setAlbums', state.allAlbums.filter((album) => album.access_level > 0));
  },

  setTags(state, tags) {
    state.tags = tags;
  },

  setTag(state, slug) {
    state.tag = state.tags.filter((tag) => tag.slug === slug)[0];
  },

  setLoading(state, loading) {
    loading ? state.loading += 1 : state.loading -= 1;
  },

  selectPhoto(state, photo) {
    state.selected.push(photo);
  },
  deselectPhoto(state, photo) {
    state.selected.remove(photo);
  },

  selectAll(state) {
    state.selected = [...state.photos];
  },
  selectInvert(state) {
    state.photos.forEach((photo) => {
      if (state.selected.includes(photo)) {
        state.selected.remove(photo)
      } else {
        state.selected.push(photo);
      }
    });
  },
  selectNone(state) {
    state.selected.clear();
  },

  clearAlbum(state) {
    state.album = {
      name: '',
      place: '',
      location: '',
      description: '',
      start: null,
      end: null,
      access_level: 0,
      access_code: '',
      users: [],
      groups: [],
      tags: [],
      parent: '',
    };
  },

  setAlbumByPath(state, path) {
    state.album = state.allAlbums.filter((album) => album.path === path)[0];
  },

  setAlbum(state, album) {
    state.album = album;
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

  clearPhotos(state) {
    state.photos = [];
  },

  updateDocumentTitleForAlbum(state) {
    document.title = titleTemplate.format(state.album.name);
  },

  updateDocumentTitleForEditAlbum(state) {
    let newTitle = editorTitleTemplate.format(state.album.name);

    // Update history entry
    if (document.title !== newTitle) {
      document.title = newTitle;

      let route = {name: 'editAlbum', params: {path: state.album.path.split('/')}};
      let resolved = router.resolve(route);
      window.history.replaceState(null, newTitle, resolved.href);
    }
  },

  setGitStatus(state, status) {
    state.gitStatus = status;
  },

  setPhotosPerPage(state, count) {
    state.photosPerPage = count;

    state.photos.forEach((photo, index) => {
      photo.page = Math.floor(index / state.photosPerPage) + 1;
    });

    this.commit('setPhotoPage', 1);
  },
};
