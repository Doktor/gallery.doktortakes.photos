import { store } from "./store";
import { fields } from "./constants";

export function addAuthorizationHeader(options) {
  if (store.state.token !== null) {
    let header = `Token ${store.state.token}`;

    if (options.hasOwnProperty("headers")) {
      options.headers["Authorization"] = header;
    } else {
      options.headers = {
        Authorization: header,
      };
    }
  }
}

export async function sendRequest(url, options = {}) {
  addAuthorizationHeader(options);

  try {
    const response = await fetch(url, options);

    const text = await response.text();
    let content = null;

    if (text.length > 0) {
      const contentType = response.headers.get("content-type");

      if (contentType.includes("application/json")) {
        content = JSON.parse(text);
      } else {
        content = text;
      }
    }

    return { ok: response.ok, status: response.status, content: content };
  } catch (error) {
    console.error(error);
  }
}

export function parseAlbumForAPI(album) {
  let data = {};

  Object.entries(album).forEach(([key, value]) => {
    // Don't send readonly fields
    if (fields.readonly.includes(key)) {
    }
    // Everything else
    else {
      data[key] = value;
    }
  });

  return data;
}

export function parseAlbumDetail(album, children) {
  album.pathSplit = album.path.split("/");
  album.tags.sort();

  for (let child of children) {
    child.pathSplit = child.path.split("/");
  }

  album.children = children;
}

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
  if (Object.keys(params).length === 0) {
    return "";
  }

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

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

Array.prototype.remove = function (item) {
  this.splice(this.indexOf(item), 1);
};

String.prototype.format = function () {
  "use strict";
  let str = this.toString();
  if (arguments.length) {
    let t = typeof arguments[0];
    let key;
    let args =
      "string" === t || "number" === t
        ? Array.prototype.slice.call(arguments)
        : arguments[0];

    for (key in args) {
      str = str.replace(new RegExp("\\{" + key + "\\}", "gi"), args[key]);
    }
  }

  return str;
};
