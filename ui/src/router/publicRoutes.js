import AboutPage from "@/pages/public/AboutPage";
import CopyrightPage from "@/pages/public/CopyrightPage";

import AlbumListPage from "@/pages/public/AlbumListPage";
import AlbumDetailPage from "@/pages/public/AlbumDetailPage";
import PhotoDetailPage from "@/pages/public/PhotoDetailPage";
import TagListPage from "@/pages/public/TagListPage";
import TagDetailPage from "@/pages/public/TagDetailPage";
import TaxonListPage from "@/pages/public/TaxonListPage";
import SpeciesListPage from "@/pages/public/SpeciesListPage";

import SearchPhotosPage from "@/pages/public/SearchPhotosPage";
import FeaturedPage from "@/pages/public/FeaturedPage";
import ExternalAlbumListPage from "@/pages/public/ExternalAlbumListPage.vue";

export const publicRoutes = [
  {
    path: "/",
    name: "index",
    component: AlbumListPage,
    meta: {
      title: "Index",
    },
  },

  {
    path: "/albums/:path+/:md5",
    strict: true,
    name: "photo",
    component: PhotoDetailPage,
    meta: {
      body: "photo-viewer",
      showNavigation: false,
    },
  },
  {
    path: "/albums/:path+/",
    strict: true,
    name: "album",
    component: AlbumDetailPage,
  },
  {
    path: "/albums/",
    redirect: {
      name: "index",
    },
  },

  {
    path: "/featured/:path+/",
    strict: true,
    name: "featuredAlbum",
    component: FeaturedPage,
  },

  {
    path: "/external/:path+/:md5",
    strict: true,
    name: "externalPhoto",
    component: PhotoDetailPage,
    meta: {
      body: "photo-viewer",
      showNavigation: false,
    },
    props: {
      isExternal: true,
    },
  },
  {
    path: "/external/:path+/",
    strict: true,
    name: "externalAlbum",
    component: AlbumDetailPage,
    props: {
      isExternal: true,
    },
  },
  {
    path: "/external/",
    name: "externalAlbums",
    component: ExternalAlbumListPage,
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
];
