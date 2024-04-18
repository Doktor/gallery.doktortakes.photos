import ManagePage from "@/pages/manage/ManagePage";
import NewAlbumPage from "@/pages/manage/NewAlbumPage";
import EditAlbumPage from "@/pages/manage/EditAlbumPage";
import EditPhotoPage from "@/pages/manage/EditPhotoPage";
import ManageTaxaPage from "@/pages/manage/ManageTaxaPage";
import UserListPage from "@/pages/manage/UserListPage";
import GroupListPage from "@/pages/manage/GroupListPage";
import NewManagePage from "@/pages/manage/NewManagePage.vue";

export const manageRoutes = [
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
    path: "/manage/new/",
    name: "manage-new",
    component: NewManagePage,
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
    name: "manageTaxa",
    component: ManageTaxaPage,
    meta: {
      staff: true,
      title: "Manage taxa",
    },
  },

  {
    path: "/manage/users/",
    name: "users",
    component: UserListPage,
    meta: {
      staff: true,
      title: "Users",
    },
  },
  {
    path: "/manage/groups/",
    name: "groups",
    component: GroupListPage,
    meta: {
      staff: true,
      title: "Groups",
    },
  },
];
