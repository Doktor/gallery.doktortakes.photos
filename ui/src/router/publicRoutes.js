import CopyrightPage from "@/pages/public/CopyrightPage";

import AlbumListPage from "@/pages/public/AlbumListPage";
import AlbumDetailPage from "@/pages/public/AlbumDetailPage";
import PhotoDetailPage from "@/pages/public/PhotoDetailPage";
import TagListPage from "@/pages/public/TagListPage";
import TagDetailPage from "@/pages/public/TagDetailPage";
import TaxonListPage from "@/pages/public/TaxonListPage";
import SpeciesListPage from "@/pages/public/SpeciesListPage";

import SearchPhotosPage from "@/pages/public/SearchPhotosPage";

export const publicRoutes = [
  {
    path: "/",
    name: "index",
    component: AlbumListPage,
  },

  {
    path: "/albums/:path+/:md5",
    strict: true,
    name: "photo",
    component: PhotoDetailPage,
    meta: {
      body: "photo-viewer",
      showNavigation: false,
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
    redirect: {
      name: "index",
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
    path: "/taxa/species/",
    name: "species",
    component: SpeciesListPage,
  },
  {
    path: "/taxa/:catalogId/",
    name: "taxaByCatalogId",
    component: TaxonListPage,
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
    path: "/copyright/",
    name: "copyright",
    component: CopyrightPage,
    meta: {
      title: "Copyright",
    },
  },
];
