import { fields } from "./constants";
import { camelToSnake } from "@/request";

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

  album.licenseId = album.license?.id ?? null;

  album.children = children;
}

export function getQueryString(params) {
  if (Object.keys(params).length === 0) {
    return "";
  }

  let escape = encodeURIComponent;

  let query = Object.entries(params)
    .map(([key, value]) => {
      const snakeKey = camelToSnake(key);

      if (Array.isArray(value) && value.length > 0) {
        return escape(snakeKey) + "=" + escape(value.join(","));
      }

      if (value !== undefined && value !== null && value !== "") {
        return escape(snakeKey) + "=" + escape(value);
      }
    })
    .filter((item) => item !== undefined);

  return "?" + query.join("&");
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function wait(ms, f) {
  return setTimeout(f, ms);
}

export function pluralize(value) {
  return value === 1 ? "" : "s";
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

export function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}
