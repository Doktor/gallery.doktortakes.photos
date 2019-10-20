import VueRouter from 'vue-router';

import {store} from "../store/index.js";

import ViewAlbum from "../views/ViewAlbum.vue";
import ViewAlbums from "../views/ViewAlbums.vue";
import ViewPhoto from "../views/ViewPhoto.vue";
import ViewFeaturedPhotos from "../views/ViewFeaturedPhotos.vue";
import ViewTags from "../views/ViewTags.vue";
import ViewTag from "../views/ViewTag.vue";
import ViewUser from "../views/ViewUser.vue";
import ChangePassword from "../views/ChangePassword.vue";

import SearchPhotos from "../views/SearchPhotos.vue";

import EditAlbum from "../views/EditAlbum.vue";
import EditAlbums from "../views/EditAlbums.vue";
import NewAlbum from "../views/NewAlbum.vue";


const browserRoutes = [
  {
    path: '/albums/',
    name: 'albums',
    component: ViewAlbums,
  },
  {
    path: '/albums/:path+/',
    name: 'album',
    component: ViewAlbum,
  },
  {
    path: '/albums/:path+/:md5',
    name: 'photo',
    component: ViewPhoto,
  },

  {
    path: '/featured/',
    name: 'featured',
    component: ViewFeaturedPhotos,
  },

  {
    path: '/tags/',
    name: 'tags',
    component: ViewTags,
  },
  {
    path: '/tags/:slug/',
    name: 'tag',
    component: ViewTag,
  },

  {
    path: '/search/',
    name: 'search',
    component: SearchPhotos,
  },

  {
    path: '/users/:slug/',
    name: 'user',
    component: ViewUser,
  },
  {
    path: '/users/:slug/password/',
    name: 'changePassword',
    component: ChangePassword,
  },
];

const editorRoutes = [
  {
    path: '/editor/',
    name: 'index',
    component: EditAlbums,
    meta: {
      staff: true,
    },
  },
  {
    path: '/editor/albums/new/',
    name: 'newAlbum',
    component: NewAlbum,
    meta: {
      staff: true,
    },
  },
  {
    path: '/editor/albums/edit/:path+/',
    name: 'editAlbum',
    component: EditAlbum,
    meta: {
      staff: true,
    },
  },
];

const routes = browserRoutes.concat(editorRoutes);
routes.forEach((route) => route.pathToRegexpOptions = {strict: true});

const router = new VueRouter({
  mode: 'history',
  routes,
});

router.beforeEach((to, from, next) => {
  store.dispatch('getUser').then(() => {
    if (to.matched.some(record => record.meta.staff)) {
      let user = store.state.user;

      if (user.status === 'staff' || user.status === 'superuser') {
        next();
      } else {
        next({
          path: '/log-in/',
          query: {
            redirect: to.fullPath,
          },
        });
      }
    } else {
      next();
    }
  })
});


export {router};
