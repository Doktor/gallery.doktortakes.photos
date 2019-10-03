import VueRouter from 'vue-router';

import ViewAlbum from "../views/ViewAlbum.vue";
import ViewAlbums from "../views/ViewAlbums.vue";
import ViewPhoto from "../views/ViewPhoto.vue";


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
    path: '/albums/:path+/:md5',
    name: 'photo',
    component: ViewPhoto,
    pathToRegexpOptions: {
      strict: true,
    },
  },
];


export const router = new VueRouter({
  mode: 'history',
  routes,
});
