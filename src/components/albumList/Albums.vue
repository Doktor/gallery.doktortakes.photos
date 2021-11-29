<template>
  <section>
    <AlbumListViewSelector v-if="isStaff"/>

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

    <PaginationAlbums
        v-if="!isSkeleton"
        :albumsPerPage="albumsPerPage"
        :page="page"
        :pages="albumPages"
        @setAlbumPage="setAlbumPage"
        @setAlbumsPerPage="setAlbumsPerPage"
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
  import PaginationAlbums from '@/components/pagination/PaginationAlbums.vue';


  export default {
    components: {
      AlbumListCards,
      AlbumCard,
      AlbumListSimple,
      AlbumListViewSelector,
      AlbumTable,
      PaginationAlbums,
    },

    computed: {
      ...mapGetters([
        "isStaff",
        "albumPages",
      ]),
      ...mapState([
        'albumsPerPage',
        'page',
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
        this.$store.commit('setAlbumPage', page);
      },
      setAlbumsPerPage(count) {
        this.$store.commit('setAlbumsPerPage', count);
      },
    },
  }
</script>
