import VueRouter from 'vue-router';

import ViewAlbum from "../views/ViewAlbum.vue";
import ViewAlbums from "../views/ViewAlbums.vue";
import ViewPhoto from "../views/ViewPhoto.vue";
import ViewTags from "../views/ViewTags.vue";
import ViewTag from "../views/ViewTag.vue";

import EditAlbum from "../views/EditAlbum.vue";
import EditAlbums from "../views/EditAlbums.vue";
import NewAlbum from "../views/NewAlbum.vue";


const browserRoutes = [
  {
    path: '/albums/',
    name: 'albums',
    component: ViewAlbums,
    pathToRegexpOptions: {
      strict: true,
    },
  },
  {
    path: '/albums/:path+/',
    name: 'album',
    component: ViewAlbum,
    pathToRegexpOptions: {
      strict: true,
    },
  },
  {
    path: '/albums/:path+/:md5',
    name: 'photo',
    component: ViewPhoto,
    pathToRegexpOptions: {
      strict: true,
    },
  },

  {
    path: '/tags/',
    name: 'tags',
    component: ViewTags,
    pathToRegexpOptions: {
      strict: true,
    },
  },
  {
    path: '/tags/:slug/',
    name: 'tag',
    component: ViewTag,
    pathToRegexpOptions: {
      strict: true,
    },
  },
];

const editorRoutes = [
  {
    path: '/editor/',
    name: 'index',
    component: EditAlbums,
  },
  {
    path: '/editor/albums/new',
    name: 'newAlbum',
    component: NewAlbum,
  },
  {
    path: '/editor/albums/edit/:path',
    name: 'editAlbum',
    component: EditAlbum,
  },
];

const routes = browserRoutes.concat(editorRoutes);


export const router = new VueRouter({
  mode: 'history',
  routes,
});
