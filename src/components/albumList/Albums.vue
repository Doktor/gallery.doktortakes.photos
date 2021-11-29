<template>
  <section>
    <AlbumListViewSelector v-if="isStaff" />

    <component
        :is="albumListComponent"
        :class="classes"

        :albums="albums"
        :route="albumRoute"
        :indexStart="indexStart"
        :indexEnd="indexEnd"
        :isSkeleton="isSkeleton"
    />

    <slot name="footer"></slot>

    <Pagination
        :itemsPerPage="albumsPerPage"
        :itemsPerPageChoices="itemsPerPageChoices"
        @setPage="setAlbumPage"
        @setItemsPerPage="setAlbumsPerPage"
        :page="page"
        :pages="pages"
    />
  </section>
</template>

<script>
import {mapGetters, mapState} from 'vuex';
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

  data() {
    return {
      albumsPerPage: 12,
      page: 1,
    }
  },

  computed: {
    ...mapGetters([
      "isStaff",
    ]),
    ...mapState([
      'results',
      'user',
    ]),

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
        "albums": this.view === undefined || this.view === "default",
        "album-list-simple": this.view === "simple",
      }
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
      return Math.ceil(this.results.length / this.albumsPerPage);
    },

    view() {
      return this.$route.query.view;
    },
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

    isSkeleton: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    setAlbumPage(page) {
      this.page = page;

      this.results.filter((album) => !album.loaded).forEach((album, index) => {
        if (page === Math.floor(index / this.albumsPerPage) + 1) {
          album.isLoaded = true;
        }
      });
    },

    setAlbumsPerPage(count) {
      this.albumsPerPage = count;
      this.setAlbumPage(1);
    },
  },

  watch: {
    results(newResults) {
      if (newResults.length) {
        this.setAlbumPage(1);
      }
    },
  },
}
</script>
