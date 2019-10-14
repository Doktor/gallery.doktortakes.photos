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


// API endpoints and static files

const api = document.getElementById('api');

export const endpoints = {
  albumList: "/api/albums/",
  albumDetail: "/api/albums/:path/",
  albumPhotoList: "/api/albums/:path/photos/",
  tagList: "/api/tags/",
  tagDetail: "/api/tags/:slug/",
  currentUser: "/api/me/",
};

export const staticFiles = {
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

    page: 1,
    loaded: [],

    settings: settings,
  },

  actions,
  getters,
  mutations,
});
