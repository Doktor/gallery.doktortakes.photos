import Vue from "vue";
import {updateField} from "vuex-map-fields";
import {getQueryString} from "./index.js";
import {router} from "@/router/main.js";


const titleTemplate = "{0} | Doktor Takes Photos";
const editorTitleTemplate = "Editing {0} | Doktor Takes Photos";

const photoTitleTemplate = "{0} | {1} | Doktor Takes Photos";


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

  setUsers(state, users) {
    state.users = users;
  },

  setGroups(state, groups) {
    state.groups = groups;
  },

  setUser(state, user) {
    state.user = user;
  },

  setAlbumPage(state, page) {
    state.page = page;
    state.results.filter((album) => !album.loaded).forEach((album, index) => {
      if (page === Math.floor(index / state.albumsPerPage) + 1) {
        album.isLoaded = true;
      }
    });
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
    this.commit('setAlbumPage', 1);
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

  setPhotoInitial(state, {md5, code = ""}) {
    let photo = state.photos.filter((photo) => photo.md5 === md5)[0];
    this.commit('setPhoto', {index: photo.index, code: code});
  },

  setPhoto(state, {index, history = true, code = ""}) {
    if (index === state.photo.index) {
      return;
    }

    // Wrap around
    if (index < 0) {
      index = state.photos.length - 1;
    } else if (index > state.photos.length - 1) {
      index = 0;
    }

    let photo = state.photos[index];
    photo.loaded = true;

    state.photo = photo;

    let length = state.photos.length;

    // Preload previous 2 and next 2 photos
    let prev = (photo.index - 2 + length) % length;

    for (let i = prev; i < prev + 5; i++) {
      let photo = state.photos[i % length];

      if (!photo.loaded) {
        this.commit('preloadPhoto', photo);
      }
    }

    if (history) {
      let title = photoTitleTemplate.format(photo.md5.substring(0, 8), state.album.name);
      document.title = title;

      let qs = code ? getQueryString({code: code}) : "";
      window.history.pushState(null, title, photo.url + qs);
    }
  },

  preloadPhoto(state, photo) {
    if (!photo.loaded) {
      let image = new Image();
      image.src = photo.image;

      photo.loaded = true;
    }
  },

  updateDocumentTitleForAlbum(state) {
    document.title = titleTemplate.format(state.album.name);
  },

  updateDocumentTitleForEditAlbum(state) {
    let newTitle = editorTitleTemplate.format(state.album.name);

    // Update history entry
    if (document.title !== newTitle) {
      document.title = newTitle;

      let url = router.resolve({name: 'editAlbum', params: {path: state.album.path}});
      window.history.replaceState(null, newTitle, url);
    }
  },

  setGitStatus(state, status) {
    state.gitStatus = status;
  },

  updateAlbumPhotosCache(state, {path, photos}) {
    Vue.set(state.albumPhotosCache, path, photos);
  },

  setAlbumsPerPage(state, count) {
    state.albumsPerPage = count;
    this.commit('setAlbumPage', 1);
  },

  setPhotosPerPage(state, count) {
    state.photosPerPage = count;

    state.photos.forEach((photo, index) => {
      photo.page = Math.floor(index / state.photosPerPage) + 1;
    });

    this.commit('setPhotoPage', 1);
  },
};
