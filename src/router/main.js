import VueRouter from 'vue-router';

import {store} from "../store/index.js";

import Index from "../views/Index.vue";

import AlbumList from "../views/AlbumList.vue";
import AlbumDetail from "../views/AlbumDetail.vue";
import PhotoDetail from "../views/PhotoDetail.vue";
import FeaturedPhotos from "../views/FeaturedPhotos.vue";
import TagList from "../views/TagList.vue";
import TagDetail from "../views/TagDetail.vue";
import UserList from "../views/UserList.vue";
import UserDetail from "../views/UserDetail.vue";
import ChangePassword from "../views/ChangePassword.vue";

import About from "../views/About.vue";
import Copyright from "../views/Copyright.vue";
import Recent from "../views/Recent.vue";

import SearchPhotos from "../views/SearchPhotos.vue";

import EditAlbum from "../views/EditAlbum.vue";
import EditAlbums from "../views/EditAlbums.vue";
import NewAlbum from "../views/NewAlbum.vue";


export const baseTitle = "Doktor Takes Photos";

const browserRoutes = [
  {
    path: '/',
    name: 'index',
    component: Index,
  },

  {
    path: '/albums/',
    name: 'albums',
    component: AlbumList,
    meta: {
      title: "Albums",
    },
  },
  {
    path: '/albums/:path+/',
    name: 'album',
    component: AlbumDetail,
    meta: {
      title: false,
    },
  },
  {
    path: '/albums/:path+/:md5',
    name: 'photo',
    component: PhotoDetail,
    meta: {
      body: 'photo-viewer',
      nav: false,
      title: false,
    },
  },

  {
    path: '/featured/',
    name: 'featured',
    component: FeaturedPhotos,
    meta: {
      title: "Featured",
    },
  },

  {
    path: '/tags/',
    name: 'tags',
    component: TagList,
    meta: {
      title: "Tags",
    },
  },
  {
    path: '/tags/:slug/',
    name: 'tag',
    component: TagDetail,
    meta: {
      title: false,
    },
  },

  {
    path: '/search/',
    name: 'search',
    component: SearchPhotos,
    meta: {
      title: "Search",
    },
  },

  {
    path: '/users/',
    name: 'users',
    component: UserList,
    meta: {
      staff: true,
      title: "Users",
    },
  },
  {
    path: '/users/:slug/',
    name: 'user',
    component: UserDetail,
    meta: {
      title: false,
    },
  },
  {
    path: '/users/:slug/password/',
    name: 'changePassword',
    component: ChangePassword,
    meta: {
      title: "Change your password",
    },
  },

  {
    path: '/about/',
    name: 'about',
    component: About,
    meta: {
      title: "About",
    },
  },
  {
    path: '/copyright/',
    name: 'copyright',
    component: Copyright,
    meta: {
      title: "Copyright",
    },
  },

  {
    path: '/recent/',
    name: 'recent',
    component: Recent,
    meta: {
      title: "Recent changes",
    },
  }
];

const editorRoutes = [
  {
    path: '/editor/',
    name: 'editorIndex',
    component: EditAlbums,
    meta: {
      staff: true,
      title: "Edit albums",
    },
  },
  {
    path: '/editor/albums/new/',
    name: 'newAlbum',
    component: NewAlbum,
    meta: {
      staff: true,
      title: "Create new album",
    },
  },
  {
    path: '/editor/albums/edit/:path+/',
    name: 'editAlbum',
    component: EditAlbum,
    meta: {
      staff: true,
      title: "Edit album: {album}",
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

router.afterEach((to, from) => {
  if (to.name !== from.name) {
    window.scrollTo(0, 0);
  }

  for (let record of to.matched) {
    // <body>
    let body = record.meta.body;

    if (body === undefined) {
      document.body.className = "";
    } else {
      document.body.className = body;
    }

    // .nav
    let nav = document.querySelector('.nav');

    if (nav !== null) {
      nav.classList.toggle('hidden', record.meta.nav === false);
    }

    // Document title
    let title = record.meta.title;

    if (title === false) {
      // Don't change the title
    } else if (title !== undefined) {
      document.title = title + " | " + baseTitle;
    } else {
      document.title = baseTitle;
    }
  }
});


export {router};
