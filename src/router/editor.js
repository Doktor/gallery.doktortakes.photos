import VueRouter from 'vue-router';

import EditAlbum from "../views/EditAlbum.vue";
import EditAlbums from "../views/EditAlbums.vue";
import NewAlbum from "../views/NewAlbum.vue";


const routes = [
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


export const router = new VueRouter({
  mode: 'history',
  routes,
});
