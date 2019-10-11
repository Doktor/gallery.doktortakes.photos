<template>
  <section>
    <Pagination :mutation="'setAlbumPage'" :itemsPerPage="albumsPerPage" :page="page" :pages="albumPages"/>
    <section class="albums">
      <AlbumCard
          v-for="(album, index) in albums"
          :album="album"
          :isLoaded="album.isLoaded"
          :isVisible="indexStart <= index && index <= indexEnd"
          :key="album.path"
          :route="route"
      />
    </section>
    <Pagination :mutation="'setAlbumPage'" :itemsPerPage="albumsPerPage" :page="page" :pages="albumPages"/>
  </section>
</template>

<script>
  import AlbumCard from "./AlbumCard.vue";
  import Pagination from './Pagination.vue';
  import {mapGetters, mapState} from 'vuex';


  export default {
    components: {
      AlbumCard,
      Pagination,
    },

    computed: {
      indexStart() {
        return this.albumsPerPage * (this.page - 1);
      },
      indexEnd() {
        return this.indexStart + this.albumsPerPage - 1;
      },

      ...mapGetters([
        'albumsPerPage',
        'albumPages',
      ]),
      ...mapState([
        'page',
      ]),
    },

    props: {
      albums: {
        type: Array,
        required: true,
      },
      route: {
        type: String,
        default: "album",
      }
    }
  }
</script>
