<template>
  <section>
    <Pagination
        v-if="allowPagination"
        :mutation="'setAlbumPage'"
        :itemsPerPage="albumsPerPage"
        :page="page"
        :pages="albumPages"/>

    <AlbumListViewSelector/>

    <section v-if="view === undefined || view === 'default'" class="albums">
      <AlbumCard
          v-for="(album, index) in albums"
          :album="album"
          :isLoaded="album.isLoaded"
          :isVisible="indexStart <= index && index <= indexEnd"
          :key="album.path"
          :route="albumRoute"
      />
    </section>
    <section v-else-if="view === 'detailed'" class="album-list-dc">
      <AlbumListDetailedCards :albums="albums" :route="albumRoute"/>
    </section>
    <section v-else-if="view === 'simple'">
      <AlbumListSimple :albums="albums" :route="albumRoute"/>
    </section>

    <Pagination
        v-if="allowPagination"
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
  import AlbumListDetailedCards from "../components/AlbumListDetailedCards.vue";
  import AlbumListSimple from "../components/AlbumListSimple.vue";
  import AlbumListViewSelector from "../components/AlbumListViewSelector.vue";


  export default {
    components: {
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

      allowPagination() {
        return this.view === undefined || this.view === 'default';
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
