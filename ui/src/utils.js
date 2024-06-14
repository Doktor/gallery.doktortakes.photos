import { fields } from "./constants";

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

export function wait(ms, f) {
  return setTimeout(f, ms);
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
