<template>
  <section>
    <Pagination
        :mutation="'setAlbumPage'"
        :itemsPerPage="albumsPerPage"
        :page="page"
        :pages="albumPages"/>

    <AlbumListViewSelector/>

    <section>
      <component
          :is="albumListComponent"
          :class="classes"

          :albums="albums"
          :route="albumRoute"
          :indexStart="indexStart"
          :indexEnd="indexEnd"
      />
    </section>

    <Pagination
        :mutation="'setAlbumPage'"
        :itemsPerPage="albumsPerPage"
        :page="page"
        :pages="albumPages"/>
  </section>
</template>

<script>
  import {mapGetters, mapState} from 'vuex';
  import AlbumCard from "./AlbumCard.vue";
  import Pagination from './Pagination.vue';
  import AlbumListCards from "./AlbumListCards.vue";
  import AlbumListDetailedCards from "../components/AlbumListDetailedCards.vue";
  import AlbumListSimple from "../components/AlbumListSimple.vue";
  import AlbumListViewSelector from "../components/AlbumListViewSelector.vue";


  export default {
    components: {
      AlbumListCards,
      AlbumCard,
      AlbumListDetailedCards,
      AlbumListSimple,
      AlbumListViewSelector,
      Pagination,
    },

    computed: {
      ...mapGetters([
        'albumsPerPage',
        'albumPages',
      ]),
      ...mapState([
        'page',
      ]),

      albumListComponent() {
        switch (this.view) {
          case "detailed":
            return "AlbumListDetailedCards";
          case "simple":
            return "AlbumListSimple";
          default:
            return "AlbumListCards";
        }
      },

      classes() {
        return {
          "albums": this.view === undefined || this.view === "default",
          "album-list-simple": this.view === "simple",
          "album-list-dc": this.view === "detailed",
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
      }
    }
  }
</script>
