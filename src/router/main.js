import VueRouter from "vue-router";

import { store } from "../store/index.js";

import Index from "../pages/Index.vue";

import AlbumList from "../pages/AlbumList.vue";
import AlbumDetail from "../pages/AlbumDetail.vue";
import PhotoDetail from "../pages/PhotoDetail.vue";
import TagList from "../pages/TagList.vue";
import TagDetail from "../pages/TagDetail.vue";
import UserList from "../pages/UserList.vue";
import UserDetail from "../pages/UserDetail.vue";
import ChangePassword from "../pages/ChangePassword.vue";

import GroupList from "../pages/GroupList.vue";

import About from "../pages/About.vue";
import Copyright from "../pages/Copyright.vue";
import Recent from "../pages/Recent.vue";

import SearchPhotos from "../pages/SearchPhotos.vue";

import EditAlbum from "../pages/EditAlbum.vue";
import Manage from "../pages/Manage.vue";
import NewAlbum from "../pages/NewAlbum.vue";

import LogIn from "@/pages/LogIn";
import LogOut from "@/pages/LogOut";
import EditPhoto from "@/pages/EditPhoto";

export const baseTitle = "Doktor Takes Photos";

const browserRoutes = [
  {
    path: "/",
    name: "index",
    component: Index,
  },

  {
    path: "/albums/:path+/:md5/",
    name: "photo",
    component: PhotoDetail,
    meta: {
      body: "photo-viewer",
      nav: false,
      title: false,
    },
  },
  {
    path: "/albums/:path+/",
    name: "album",
    component: AlbumDetail,
    meta: {
      title: false,
    },
  },
  {
    path: "/albums/",
    name: "albums",
    component: AlbumList,
    meta: {
      title: "Albums",
    },
  },

  {
    path: "/tags/",
    name: "tags",
    component: TagList,
    meta: {
      title: "Tags",
    },
  },
  {
    path: "/tags/:slug/",
    name: "tag",
    component: TagDetail,
    meta: {
      title: false,
    },
  },

  {
    path: "/search/",
    name: "search",
    component: SearchPhotos,
    meta: {
      title: "Search",
    },
  },

  {
    path: "/users/",
    name: "users",
    component: UserList,
    meta: {
      staff: true,
      title: "Users",
    },
  },
  {
    path: "/users/:slug/",
    name: "user",
    component: UserDetail,
    meta: {
      title: false,
    },
  },
  {
    path: "/users/:slug/password/",
    name: "changePassword",
    component: ChangePassword,
    meta: {
      title: "Change your password",
    },
  },

  {
    path: "/groups/",
    name: "groups",
    component: GroupList,
    meta: {
      staff: true,
      title: "Groups",
    },
  },

  {
    path: "/about/",
    name: "about",
    component: About,
    meta: {
      title: "About",
    },
  },
  {
    path: "/copyright/",
    name: "copyright",
    component: Copyright,
    meta: {
      title: "Copyright",
    },
  },

  {
    path: "/recent/",
    name: "recent",
    component: Recent,
    meta: {
      title: "Recent changes",
    },
  },

  {
    path: "/log-in/",
    name: "logIn",
    component: LogIn,
    meta: {
      title: "Log in",
    },
  },
  {
    path: "/log-out/",
    name: "logOut",
    component: LogOut,
    meta: {
      title: "Log out",
    },
  },
];

const manageRoutes = [
  {
    path: "/manage/",
    name: "manage",
    component: Manage,
    meta: {
      staff: true,
      title: "Manage",
    },
  },
  {
    path: "/manage/albums/new/",
    name: "newAlbum",
    component: NewAlbum,
    meta: {
      staff: true,
      title: "Create new album",
    },
  },
  {
    path: "/manage/albums/:path+/",
    name: "editAlbum",
    component: EditAlbum,
    meta: {
      staff: true,
      title: "Edit album: {album}",
    },
  },
  {
    path: "/manage/albums/:path+/photos/:md5",
    name: "editPhoto",
    component: EditPhoto,
    meta: {
      staff: true,
      title: "Edit photo: {md5}",
    },
  },
];

const routes = browserRoutes.concat(manageRoutes);
routes.forEach((route) => (route.pathToRegexpOptions = { strict: true }));

const router = new VueRouter({
  mode: "history",
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.matched.some((record) => record.meta.staff)) {
    let user = store.state.user;

    if (user.status === "staff" || user.status === "superuser") {
      next();
    } else {
      next({
        name: "logIn",
        query: {
          redirect: to.fullPath,
        },
      });
    }
  } else {
    next();
  }
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

    store.state.showNav = record.meta?.nav ?? true;

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

export { router };
