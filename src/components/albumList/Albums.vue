<template>
  <section>
    <AlbumListViewSelector v-if="userIsStaff"/>

    <PaginationAlbums v-if="!isSkeleton"/>

    <section>
      <component
          :is="albumListComponent"
          :class="classes"

          :albums="albums"
          :route="albumRoute"
          :indexStart="indexStart"
          :indexEnd="indexEnd"
          :isSkeleton="isSkeleton"
      />
    </section>

    <PaginationAlbums v-if="!isSkeleton"/>
  </section>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumCard from "./AlbumCard.vue";
  import AlbumListCards from "./AlbumListCards.vue";
  import AlbumListSimple from "./AlbumListSimple.vue";
  import AlbumListViewSelector from "./AlbumListViewSelector.vue";
  import AlbumTable from "./AlbumTable.vue";
  import PaginationAlbums from '../pagination/PaginationAlbums.vue';


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
            return this.userIsStaff ? "AlbumTable" : "AlbumListCards";
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
      },

      isSkeleton: {
        type: Boolean,
        default: false,
      },
    }
  }
</script>
