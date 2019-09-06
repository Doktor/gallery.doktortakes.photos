import {updateField} from "vuex-map-fields";
import Vue from "vue";
import {fields} from "./index.js";


const titleTemplate = "Editing {0} | Doktor Takes Photos";


export const mutations = {
  // vuex-map-fields
  updateField,

  changePage(state, page) {
    state.page = page;
    state.loaded.push(page);
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
      photo.page = Math.floor(index / state.settings.itemsPerPage) + 1;
    }

    state.photos = photos;
  }
};
