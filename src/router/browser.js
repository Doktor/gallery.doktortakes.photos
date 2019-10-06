import VueRouter from 'vue-router';

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
    path: '/albums/:path/',
    name: 'album',
  },
  {
    path: '/albums/:path/:md5',
    name: 'photo',
  }
];


export const router = new VueRouter({
  mode: 'history',
  routes,
});
