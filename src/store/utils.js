import { fields, store } from "@/store/index";


export function addAuthorizationHeader(options) {
  if (store.state.token !== null) {
    let header = `Token ${store.state.token}`;

    if (options.hasOwnProperty("headers")) {
      options.headers['Authorization'] = header
    } else {
      options.headers = {
        'Authorization': header,
      }
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
      const contentType = response.headers.get('content-type');

      if (contentType.includes('application/json')) {
        content = JSON.parse(text);
      } else {
        content = text;
      }
    }

    return { ok: response.ok, status: response.status, content: content }
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
