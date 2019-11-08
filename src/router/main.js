import VueRouter from 'vue-router';

import {store} from "../store/index.js";

import ViewIndex from "../views/ViewIndex.vue";

import ViewAlbum from "../views/ViewAlbum.vue";
import ViewAlbums from "../views/ViewAlbums.vue";
import ViewPhoto from "../views/ViewPhoto.vue";
import ViewFeaturedPhotos from "../views/ViewFeaturedPhotos.vue";
import ViewTags from "../views/ViewTags.vue";
import ViewTag from "../views/ViewTag.vue";
import ViewUser from "../views/ViewUser.vue";
import ChangePassword from "../views/ChangePassword.vue";

import ViewAbout from "../views/ViewAbout.vue";
import ViewCopyright from "../views/ViewCopyright.vue";
import ViewRecent from "../views/ViewRecent.vue";

import SearchPhotos from "../views/SearchPhotos.vue";

import EditAlbum from "../views/EditAlbum.vue";
import EditAlbums from "../views/EditAlbums.vue";
import NewAlbum from "../views/NewAlbum.vue";


const baseTitle = "Doktor Takes Photos";

const browserRoutes = [
  {
    path: '/',
    name: 'index',
    component: ViewIndex,
  },

  {
    path: '/albums/',
    name: 'albums',
    component: ViewAlbums,
    meta: {
      body: 'small',
      title: "Albums",
    },
  },
  {
    path: '/albums/:path+/',
    name: 'album',
    component: ViewAlbum,
    meta: {
      title: false,
    },
  },
  {
    path: '/albums/:path+/:md5',
    name: 'photo',
    component: ViewPhoto,
    meta: {
      body: 'photo-viewer',
      nav: false,
      title: false,
    },
  },

  {
    path: '/featured/',
    name: 'featured',
    component: ViewFeaturedPhotos,
    meta: {
      title: "Featured",
    },
  },

  {
    path: '/tags/',
    name: 'tags',
    component: ViewTags,
    meta: {
      body: 'small',
      title: "Tags",
    },
  },
  {
    path: '/tags/:slug/',
    name: 'tag',
    component: ViewTag,
    meta: {
      body: 'small',
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
    path: '/users/:slug/',
    name: 'user',
    component: ViewUser,
    meta: {
      body: 'small',
      title: false,
    },
  },
  {
    path: '/users/:slug/password/',
    name: 'changePassword',
    component: ChangePassword,
    meta: {
      body: 'small',
      title: "Change your password",
    },
  },

  {
    path: '/about/',
    name: 'about',
    component: ViewAbout,
    meta: {
      body: 'small',
      title: "About",
    },
  },
  {
    path: '/copyright/',
    name: 'copyright',
    component: ViewCopyright,
    meta: {
      body: 'small',
      title: "Copyright",
    },
  },

  {
    path: '/recent/',
    name: 'recent',
    component: ViewRecent,
    meta: {
      body: 'small',
      title: "Recent changes",
    },
  }
];

const editorRoutes = [
  {
    path: '/editor/',
    name: 'index',
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
      body: 'small',
      staff: true,
      title: "Create new album",
    },
  },
  {
    path: '/editor/albums/edit/:path+/',
    name: 'editAlbum',
    component: EditAlbum,
    meta: {
      body: 'small',
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
