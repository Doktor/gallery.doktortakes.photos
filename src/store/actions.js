import {endpoints, getCsrfToken, getQueryString} from "./index.js";
import {router} from "../router/main.js";
import {sendRequest} from "@/store/utils";


export const actions = {
  async ensureCsrfToken(context) {
    await sendRequest(endpoints.csrf);
  },

  async authenticate(context, {username, password}) {
    return await sendRequest(endpoints.authenticate, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({username, password}),
    });
  },

  async getUsers(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.userList);
    let users = content.users.sort((a, b) => a.id - b.id);

    context.commit('setLoading', false);
    return users;
  },

  async getUser(context) {
    let options = {};
    let token = context.state.token;

    if (token !== null) {
      options.headers = {'Authorization': `Token ${token}`};
    }

    let {content} = await sendRequest(endpoints.currentUser, options);
    context.commit('setUser', content);
  },

  async getGroups(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.groupList);
    let groups = content.groups.sort((a, b) => a.id - b.id);

    context.commit('setLoading', false);
    return groups;
  },

  async changePassword(context, data) {
    let {ok, content} = await sendRequest(endpoints.changePassword, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    });

    if (ok) {
      context.commit('addNotification', content.message);

      setTimeout(() => router.push({
        name: 'user',
        params: {
          slug: context.state.user.name
        },
      }), 1000);

      return;
    }

    content.errors.forEach((error) => {
      context.commit('addNotification', error);
    });
  },

  async getAllAlbums(context) {
    if (context.state.allAlbums.length > 0) {
      return Promise.resolve();
    }

    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.albumList);
    context.commit('setAllAlbums', content.albums);
    context.commit('setLoading', false);
  },

  async getAlbum(context, {rawPath, code}) {
    context.commit('setLoading', true);

    let path = Array.isArray(rawPath) ? rawPath.join('/') : rawPath;

    if (code) {
      return await context.dispatch('getAlbumWithAccessCode', {path, code})
    }

    await context.dispatch('getAllAlbums');

    let {ok, content} = await sendRequest(endpoints.albumPhotoList.replace(":path", path));

    if (!ok) {
      return false;
    }

    context.commit('setPhotos', content.photos);
    context.commit('setAlbumByPath', path);

    context.commit('setLoading', false);
    return true;
  },

  async getAlbumWithAccessCode(context, {path, code}) {
    let qs = getQueryString({code});

    let {ok, content} = await sendRequest(endpoints.albumDetail.replace(":path", path) + qs);

    if (!ok) {
      return false;
    }
    context.commit('setAlbum', content);

    let {content2} = await sendRequest(endpoints.albumPhotoList.replace(":path", path) + qs);
    context.commit('setPhotos', content2.photos);

    context.commit('setLoading', false);
    return true;
  },

  async getTags(context) {
    context.commit('setLoading', true);
    let {content} = await sendRequest(endpoints.tagList);
    context.commit('setLoading', false);

    return content.tags;
  },

  async getTag(context, slug) {
    context.commit('setLoading', true);
    let tags = await context.dispatch('getTags');
    context.commit('setLoading', false);

    return tags.find(tag => tag.slug === slug);
  },

  async getFeaturedPhotos(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.featuredPhotos);
    let photos = content.photos;

    photos.forEach((photo, index) => {
      photo.index = index;
    });

    context.commit('setLoading', false);
    context.commit('setPhotos', photos);
    context.commit('setPhoto', {index: 0, history: false});
  },

  async searchPhotos(context, queryString) {
    let {content} = await sendRequest(endpoints.searchPhotos + queryString);
    context.commit('setSearchResults', content.photos);
    context.commit('setSearchResultsCount', content.count);
    context.commit('setPhotoPage', content.page);
  },

  async getRecent(context) {
    context.commit('setLoading', true);

    let {content} = await sendRequest(endpoints.recent);
    context.commit('setAlbums', content.recent_albums);
    context.commit('setGitStatus', content.git_status);
    context.commit('setLoading', false);
  },

  async getHeroPhotos(context) {
    let {content} = await sendRequest(endpoints.heroPhotoList);
    return content;
  },
};
