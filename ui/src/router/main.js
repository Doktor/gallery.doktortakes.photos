import VueRouter from "vue-router";

import { store } from "../store";

import IndexPage from "../pages/public/IndexPage.vue";

import AlbumListPage from "../pages/public/AlbumListPage.vue";
import AlbumDetailPage from "../pages/public/AlbumDetailPage.vue";
import PhotoDetailPage from "../pages/public/PhotoDetailPage.vue";
import TagListPage from "../pages/public/TagListPage.vue";
import TagDetailPage from "../pages/public/TagDetailPage.vue";
import UserListPage from "../pages/manage/UserListPage.vue";
import UserDetailPage from "../pages/user/UserDetailPage.vue";
import ChangePasswordPage from "../pages/user/ChangePasswordPage.vue";

import GroupListPage from "../pages/manage/GroupListPage.vue";

import AboutPage from "../pages/public/AboutPage.vue";
import CopyrightPage from "../pages/public/CopyrightPage.vue";

import SearchPhotosPage from "../pages/public/SearchPhotosPage.vue";

import EditAlbumPage from "../pages/manage/EditAlbumPage.vue";
import ManagePage from "../pages/manage/ManagePage.vue";
import NewAlbumPage from "../pages/manage/NewAlbumPage.vue";

import LogInPage from "../pages/user/LogInPage.vue";
import LogOutPage from "../pages/user/LogOutPage.vue";
import EditPhotoPage from "../pages/manage/EditPhotoPage.vue";
import DebugNotificationsPage from "../pages/debug/DebugNotificationsPage.vue";
import EditTaxaPage from "../pages/manage/ManageTaxaPage.vue";

export const baseTitle = "Doktor Takes Photos";

const browserRoutes = [
  {
    path: "/",
    name: "index",
    component: IndexPage,
  },

  {
    path: "/albums/:path+/:md5",
    strict: true,
    name: "photo",
    component: PhotoDetailPage,
    meta: {
      body: "photo-viewer",
      nav: false,
      title: false,
    },
  },
  {
    path: "/albums/:path+/",
    strict: true,
    name: "album",
    component: AlbumDetailPage,
    meta: {
      title: false,
    },
  },
  {
    path: "/albums/",
    name: "albums",
    component: AlbumListPage,
    meta: {
      title: "Albums",
    },
  },

  {
    path: "/tags/",
    name: "tags",
    component: TagListPage,
    meta: {
      title: "Tags",
    },
  },
  {
    path: "/tags/:slug/",
    name: "tag",
    component: TagDetailPage,
    meta: {
      title: false,
    },
  },

  {
    path: "/search/",
    name: "search",
    component: SearchPhotosPage,
    meta: {
      title: "Search",
    },
  },

  {
    path: "/users/",
    name: "users",
    component: UserListPage,
    meta: {
      staff: true,
      title: "Users",
    },
  },
  {
    path: "/users/:slug/",
    name: "user",
    component: UserDetailPage,
    meta: {
      title: false,
    },
  },
  {
    path: "/users/:slug/password/",
    name: "changePassword",
    component: ChangePasswordPage,
    meta: {
      title: "Change your password",
    },
  },

  {
    path: "/groups/",
    name: "groups",
    component: GroupListPage,
    meta: {
      staff: true,
      title: "Groups",
    },
  },

  {
    path: "/about/",
    name: "about",
    component: AboutPage,
    meta: {
      title: "About",
    },
  },
  {
    path: "/copyright/",
    name: "copyright",
    component: CopyrightPage,
    meta: {
      title: "Copyright",
    },
  },

  {
    path: "/log-in/",
    name: "logIn",
    component: LogInPage,
    meta: {
      title: "Log in",
    },
  },
  {
    path: "/log-out/",
    name: "logOut",
    component: LogOutPage,
    meta: {
      title: "Log out",
    },
  },
];

const manageRoutes = [
  {
    path: "/manage/",
    name: "manage",
    component: ManagePage,
    meta: {
      staff: true,
      title: "Manage",
    },
  },
  {
    path: "/manage/albums/new/",
    name: "newAlbum",
    component: NewAlbumPage,
    meta: {
      staff: true,
      title: "Create new album",
    },
  },
  {
    path: "/manage/albums/:path+/",
    name: "editAlbum",
    component: EditAlbumPage,
    meta: {
      staff: true,
      title: "Edit album: {album}",
    },
  },
  {
    path: "/manage/albums/:path+/photos/:md5",
    name: "editPhoto",
    component: EditPhotoPage,
    meta: {
      staff: true,
      title: "Edit photo: {md5}",
    },
  },
  {
    path: "/manage/taxa/",
    name: "editTaxa",
    component: EditTaxaPage,
    meta: {
      staff: true,
      title: "Edit taxa",
    },
  },
];

const debugRoutes = [
  {
    path: "/debug/notifications",
    name: "debugNotifications",
    component: DebugNotificationsPage,
    meta: {
      staff: true,
      title: "Debug | Notifications",
    },
  },
];

const routes = [...browserRoutes, ...manageRoutes, ...debugRoutes];
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
