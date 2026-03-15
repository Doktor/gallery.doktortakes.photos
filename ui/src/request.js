import { store } from "@/store";

function addAuthorizationHeader(options) {
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

function modifyKeys(item, f) {
  if (Array.isArray(item)) {
    return item.map((el) => modifyKeys(el, f));
  }

  if (typeof item === "object" && item !== null) {
    return Object.fromEntries(
      Object.entries(item).map(([key, value]) => [
        f(key),
        modifyKeys(value, f),
      ]),
    );
  }

  return item;
}

export function snakeToCamel(str) {
  return str.replace(/(_[a-z])/gi, (c) => c.toUpperCase().replace(/_/g, ""));
}

function convertSnakeKeysToCamel(item) {
  return modifyKeys(item, snakeToCamel);
}

export function camelToSnake(str) {
  return str.replace(/[A-Z]/g, (c) => `_${c.toLowerCase()}`);
}

function convertCamelKeysToSnake(item) {
  return modifyKeys(item, camelToSnake);
}

export async function getAsync(url, options) {
  return await sendRequestAsync(url, options);
}

export async function postAsync(url, body) {
  return await sendWriteRequestAsync("POST", url, body);
}

export async function patchAsync(url, body) {
  return await sendWriteRequestAsync("PATCH", url, body);
}

export async function putAsync(url, body) {
  return await sendWriteRequestAsync("PUT", url, body);
}

export async function deleteAsync(url, body = null) {
  return await sendWriteRequestAsync("DELETE", url, body);
}

async function sendWriteRequestAsync(method, url, body) {
  return await sendRequestAsync(url, {
    method,
    body: JSON.stringify(convertCamelKeysToSnake(body)),
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "X-CSRFToken": getCsrfToken(),
    },
  });
}

async function sendRequestAsync(url, options = {}) {
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

    if (typeof content === "object" && content !== null) {
      content = convertSnakeKeysToCamel(content);
    }

    return { ok: response.ok, status: response.status, content };
  } catch (error) {
    console.error(error);
  }
}
