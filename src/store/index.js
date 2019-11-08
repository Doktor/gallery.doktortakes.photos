import Vue from "vue";
import Vuex from "vuex";
import {actions} from "./actions";
import {getters} from "./getters";
import {mutations} from "./mutations";

Vue.use(Vuex);


// Helper functions

export function getCsrfToken() {
  return getCookie('csrftoken');
}

export function getQueryString(params) {
  let esc = encodeURIComponent;

  let query = Object.entries(params)
  .map(([key, value]) => {
    if (Array.isArray(value)) {
      if (value.length > 0) {
        return esc(key) + "=" + esc(value.join(","));
      }
    } else if (value !== null && value !== "") {
      return esc(key) + "=" + esc(value);
    }
  })
  .filter(item => item !== undefined);

  return "?" + query.join("&");
}


// API endpoints and static files

const api = document.getElementById('api');

export const endpoints = {
  albumList: "/api/albums/",
  albumDetail: "/api/albums/:path/",
  albumPhotoList: "/api/albums/:path/photos/",
  tagList: "/api/tags/",
  tagDetail: "/api/tags/:slug/",
  featuredPhotos: "/api/photos/featured/",
  searchPhotos: "/api/photos/search/",
  currentUser: "/api/me/",
  currentUserAlbums: "/api/me/albums/",
  changePassword: "/api/me/password/",
  recent: "/api/recent/",
};

export const staticFiles = {
  blueDog: api.dataset.staticBlueDog,
  coverPlaceholder: api.dataset.staticCoverPlaceholder,
  squareThumbnailPlaceholder: api.dataset.staticSquareThumbnailPlaceholder,
};


// Other constants

export const production = process.env.NODE_ENV === 'production';

const settings = {
  albumsPerPage: 12,
  photosPerPage: production ? 30 : 10,
};

export const accessLevels = [
  {
    level: 0,
    name: 'Public',
  },
  {
    level: 10,
    name: 'Signed in',
  },
  {
    level: 20,
    name: 'Owners',
  },
  {
    level: 30,
    name: 'Staff',
  },
  {
    level: 100,
    name: 'Superusers',
  },
];

export const accessLevelsMap = Object.assign({},
  ...accessLevels.map(({level, name}) => {return {[level]: name}}));

export const fields = {
  list: ['users', 'groups', 'tags'],
  readonly: [
    'slug', 'path', 'cover', 'children',
    'url', 'edit_url', 'admin_url',
  ],
};

export const tagline = api.dataset.tagline;


// Store

export const store = new Vuex.Store({
  state: {
    strict: !production,

    user: {},

    loading: true,

    // Albums
    albums: [],
    results: [],
    search: '',
    pagesLoaded: [],

    // Tags
    tags: [],
    tag: null,

    // Album
    album: {},
    photos: [],
    count: 0,
    selected: [],

    // Photo
    photo: {},

    // Photo search
    searchResults: {
      page: 1,
      itemsPerPage: 10,
      photos: [],
      count: 0,
    },

    page: 1,
    loaded: [],

    gitStatus: {},
    settings: settings,
  },

  actions,
  getters,
  mutations,
});
