<template>
  <section>
    <AlbumListViewSelector v-if="isStaff" />

    <component
      :is="albumListComponent"
      :class="classes"
      :albums="albumsCopy"
      :routeName="albumRoute"
      :indexStart="indexStart"
      :indexEnd="indexEnd"
      :isLoading="isLoading"
    />

    <slot name="footer"></slot>

    <Pagination
      :itemsPerPage="albumsPerPage"
      :itemsPerPageChoices="itemsPerPageChoices"
      @setPage="setPage"
      @setItemsPerPage="setAlbumsPerPage"
      :page="page"
      :pages="pages"
    />
  </section>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import AlbumCard from "./AlbumCard";
import AlbumListCards from "./AlbumListCards";
import AlbumListSimple from "./AlbumListSimple";
import AlbumListViewSelector from "./AlbumListViewSelector";
import AlbumTable from "./AlbumTable";
import Pagination from "@/components/pagination/Pagination";

export default {
  components: {
    Pagination,
    AlbumListCards,
    AlbumCard,
    AlbumListSimple,
    AlbumListViewSelector,
    AlbumTable,
  },

  props: {
    albums: {
      type: Array,
      required: true,
    },

    albumRoute: {
      type: String,
      default: "album",
    },

    isLoading: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      albumsPerPage: 12,
      page: 1,

      albumsCopy: [],
    };
  },

  computed: {
    ...mapGetters(["isStaff"]),
    ...mapState(["user"]),

    albumListComponent() {
      switch (this.view) {
        case "simple":
          return "AlbumListSimple";
        case "table":
          return this.isStaff ? "AlbumTable" : "AlbumListCards";
        default:
          return "AlbumListCards";
      }
    },

    classes() {
      return {
        "album-list-simple": this.view === "simple",
      };
    },

    indexStart() {
      return this.albumsPerPage * (this.page - 1);
    },
    indexEnd() {
      return this.indexStart + this.albumsPerPage - 1;
    },

    itemsPerPageChoices() {
      return [6, 12, 24, 48];
    },

    pages() {
      return Math.ceil(this.albumsCopy.length / this.albumsPerPage);
    },

    view() {
      return this.$route.query.view;
    },
  },

  methods: {
    setPage(page) {
      this.page = page;

      this.albumsCopy
        .filter((album) => !album.loaded)
        .forEach((album, index) => {
          if (page === Math.floor(index / this.albumsPerPage) + 1) {
            this.$set(album, "isLoaded", true);
          }
        });
    },

    setAlbumsPerPage(count) {
      this.albumsPerPage = count;
      this.setPage(1);
    },

    copyObjectArray(array) {
      return [...array].map((object) => {
        return { ...object };
      });
    },

    loadAlbums(albums) {
      this.albumsCopy = this.copyObjectArray(albums);

      if (!this.loading) {
        this.setPage(1);
      }
    },
  },

  mounted() {
    this.loadAlbums(this.albums);
  },

  watch: {
    albums(newAlbums) {
      this.loadAlbums(newAlbums);
    },
  },
};
</script>
