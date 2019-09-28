import Vue from "vue";
import {updateField} from "vuex-map-fields";
import {fields} from "./index.js";


const titleTemplate = "Editing {0} | Doktor Takes Photos";


export const mutations = {
  // vuex-map-fields
  updateField,

  setPage(state, {page, mutation}) {
    state.page = page;
    this.commit(mutation, page);
  },

  setAlbumPage(state, page) {
    state.results.filter((album) => !album.loaded).forEach((album, index) => {
      if (page === Math.floor(index / state.settings.albumsPerPage) + 1) {
        album.isLoaded = true;
      }
    });
  },

  setPhotoPage(state, page) {
    state.loaded.push(page);
  },

  filterAlbums(state) {
    let term = state.search;

    if (!term) {
      state.results = state.albums;
      return;
    }

    state.results = state.albums.filter(
      (album) => album.name.match(new RegExp(term, "i")));
    this.commit('setPage', {page: 1, mutation: 'setAlbumPage'});
  },

  setAlbums(state, albums) {
    albums.map((album) => album.isLoaded = false);

    state.albums = albums;
    state.results = state.albums;
  },

  setLoading(state, loading) {
    state.loading = loading;
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
      users: '',
      groups: '',
      tags: '',
      parent: '',
    };
  },

  setAlbum(state, album) {
    let newTitle = titleTemplate.format(album.name);

    // Update page title and browser history
    if (document.title !== newTitle) {
      document.title = newTitle;
      window.history.replaceState(null, newTitle, album.edit_url);
    }

    state.album = album;

    // Store list fields as comma-separated strings
    for (let field of fields.list) {
      state.album[field] = album[field].join(', ');
    }
  },
  setAlbumField(state, data) {
    Vue.set(state.album, data.key, data.value);
  },

  setPhotos(state, photos) {
    for (let [index, photo] of photos.entries()) {
      photo.index = index;
      photo.page = Math.floor(index / state.settings.photosPerPage) + 1;
    }

    state.photos = photos;
  }
};
