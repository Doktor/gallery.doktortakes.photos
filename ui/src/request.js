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

export async function getAsync(url, options) {
  return await sendRequest(url, options);
}

export async function postAsync(url, body) {
  return await sendRequest(url, {
    method: "POST",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "X-CSRFToken": getCsrfToken(),
    },
  });
}

export async function patchAsync(url, body) {
  return await sendRequest(url, {
    method: "PATCH",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "X-CSRFToken": getCsrfToken(),
    },
  });
}

export async function putAsync(url, body) {
  return await sendRequest(url, {
    method: "PUT",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "X-CSRFToken": getCsrfToken(),
    },
  });
}

export async function deleteAsync(url, body = null) {
  return await sendRequest(url, {
    method: "DELETE",
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "X-CSRFToken": getCsrfToken(),
    },
  });
}

async function sendRequest(url, options = {}) {
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
