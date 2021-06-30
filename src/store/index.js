import Vue from "vue";
import Vuex from "vuex";
import {actions} from "./actions";
import {getters} from "./getters";
import {mutations} from "./mutations";

Vue.use(Vuex);


// Helper functions

function getCookie(name) {
  let value = null;

  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        value = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return value;
}

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
  featuredPhotos: "/api/photos/featured/",
  searchPhotos: "/api/photos/search/",
  currentUser: "/api/me/",
  changePassword: "/api/me/password/",
  recent: "/api/recent/",
  userList: "/api/users/",
  groupList: "/api/groups/",
  csrf: "/api/csrf/",
  authenticate: "/api/authenticate/",
};


// Other constants

export const production = process.env.NODE_ENV === 'production';

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
  readonly: [
    'slug', 'path', 'cover', 'children',
    'url', 'admin_url',
  ],
};

export const tagline = api.dataset.tagline;

export const domains = {
  production: "https://doktortakes.photos",
  alpha: "https://alpha.doktortakes.photos",
}


// Store

export const store = new Vuex.Store({
  state: {
    strict: !production,

    token: null,

    users: [],
    groups: [],
    user: {},
    notifications: [],

    loading: 0,

    // Cache
    albumDetailCache: {},
    albumPhotosCache: {},

    // Albums
    allAlbums: [],
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

    // Settings
    albumsPerPage: 12,
    photosPerPage: 30,
  },

  actions,
  getters,
  mutations,
});
