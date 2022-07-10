import Vue from "vue";
import Vuex from "vuex";
import { actions } from "./actions";
import { getters } from "./getters";
import { mutations } from "./mutations";

Vue.use(Vuex);

// Helper functions

function getCookie(name) {
  let value = null;

  if (document.cookie && document.cookie !== "") {
    let cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        value = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return value;
}

export function getCsrfToken() {
  return getCookie("csrftoken");
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
    .filter((item) => item !== undefined);

  return "?" + query.join("&");
}

// API endpoints and static files

const api = document.getElementById("api");

export const endpoints = {
  albumList: "/api/albums/",
  albumDetail: "/api/albums/:path/",
  albumPhotoList: "/api/albums/:path/photos/",
  photoDetail: "/api/photos/:md5/",
  thumbnailList: "/api/photos/:md5/thumbnails/",
  tagList: "/api/tags/",
  searchPhotos: "/api/photos/search/",
  currentUser: "/api/me/",
  changePassword: "/api/me/password/",
  recent: "/api/recent/",
  userList: "/api/users/",
  groupList: "/api/groups/",
  csrf: "/api/csrf/",
  authenticate: "/api/authenticate/",
  heroPhotoList: "/api/heroPhotos/",
  randomTagline: "/api/taglines/random/",
};

// Other constants

export const production = process.env.NODE_ENV === "production";

export const accessLevels = [
  {
    value: 0,
    display: "Public",
  },
  {
    value: 10,
    display: "Signed in",
  },
  {
    value: 20,
    display: "Owners",
  },
  {
    value: 30,
    display: "Staff",
  },
  {
    value: 100,
    display: "Superusers",
  },
];

export const accessLevelsMap = Object.assign(
  {},
  ...accessLevels.map(({ value, display }) => {
    return { [value]: display };
  })
);

export const fields = {
  readonly: ["slug", "path", "cover", "children", "url", "admin_url"],
};

export const domains = {
  production: "https://gallery.doktortakes.photos",
  alpha: "https://alpha.doktortakes.photos",
};

// Store

export const store = new Vuex.Store({
  state: {
    strict: !production,

    token: null,
    showNav: true,

    user: {},
    notifications: [],

    loading: 0,

    // Album
    album: {},
    photos: [],
    count: 0,
    selected: [],

    // Photo search
    searchResults: {
      page: 1,
      itemsPerPage: 10,
      photos: [],
      count: 0,
    },

    page: 1,
    loaded: [],

    // Settings
    photosPerPage: 30,
  },

  actions,
  getters,
  mutations,
});
