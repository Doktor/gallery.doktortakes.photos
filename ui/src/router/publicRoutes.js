import IndexPage from "@/pages/public/IndexPage";

import AlbumListPage from "@/pages/public/AlbumListPage";
import AlbumDetailPage from "@/pages/public/AlbumDetailPage";
import PhotoDetailPage from "@/pages/public/PhotoDetailPage";
import TagListPage from "@/pages/public/TagListPage";
import TagDetailPage from "@/pages/public/TagDetailPage";
import UserListPage from "@/pages/manage/UserListPage";
import UserDetailPage from "@/pages/user/UserDetailPage";
import ChangePasswordPage from "@/pages/user/ChangePasswordPage";

import GroupListPage from "@/pages/manage/GroupListPage";

import AboutPage from "@/pages/public/AboutPage";
import CopyrightPage from "@/pages/public/CopyrightPage";

import SearchPhotosPage from "@/pages/public/SearchPhotosPage";

import LogInPage from "@/pages/user/LogInPage";
import LogOutPage from "@/pages/user/LogOutPage";
import TaxonListPage from "@/pages/public/TaxonListPage";

export const publicRoutes = [
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
    path: "/taxa/",
    name: "taxa",
    component: TaxonListPage,
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
