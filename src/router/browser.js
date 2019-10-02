import VueRouter from 'vue-router';

import ViewAlbum from "../views/ViewAlbum.vue";
import ViewAlbums from "../views/ViewAlbums.vue";


const routes = [
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
    path: '/albums/:path/photos/:md5',
    name: 'photo',
    pathToRegexpOptions: {
      strict: true,
    },
  },
];


export const router = new VueRouter({
  mode: 'history',
  routes,
});
