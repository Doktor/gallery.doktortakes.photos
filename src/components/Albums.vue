<template>
  <section>
    <PaginationAlbums/>

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

    <PaginationAlbums/>
  </section>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumCard from "./AlbumCard.vue";
  import AlbumListCards from "./AlbumListCards.vue";
  import AlbumListDetailedCards from "../components/AlbumListDetailedCards.vue";
  import AlbumListSimple from "../components/AlbumListSimple.vue";
  import AlbumListViewSelector from "../components/AlbumListViewSelector.vue";
  import AlbumTable from "./AlbumTable.vue";
  import PaginationAlbums from './PaginationAlbums.vue';


  export default {
    components: {
      AlbumListCards,
      AlbumCard,
      AlbumListDetailedCards,
      AlbumListSimple,
      AlbumListViewSelector,
      AlbumTable,
      PaginationAlbums,
    },

    computed: {
      ...mapState([
        'albumsPerPage',
        'page',
        'user',
      ]),

      albumListComponent() {
        switch (this.view) {
          case "detailed":
            return "AlbumListDetailedCards";
          case "simple":
            return "AlbumListSimple";
          case "table":
            return this.userIsStaff ? "AlbumTable" : "AlbumListCards";
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

      userIsStaff() {
        return this.user.status === 'staff' || this.user.status === 'superuser';
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
