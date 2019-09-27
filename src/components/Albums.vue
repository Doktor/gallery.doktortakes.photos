<template>
  <section>
    <Pagination :itemsPerPage="itemsPerPage" :page="page" :pages="pages"/>
    <section class="albums">
      <Album
          v-for="(album, index) in albums"
          :album="album"
          :isLoaded="album.isLoaded"
          :isVisible="indexStart <= index && index <= indexEnd"
          :key="album.path"
      />
    </section>
    <Pagination :itemsPerPage="itemsPerPage" :page="page" :pages="pages"/>
  </section>
</template>

<script>
  import Album from "./Album.vue";
  import Pagination from './Pagination.vue';
  import {mapGetters, mapState} from 'vuex';


  export default {
    components: {
      Album,
      Pagination,
    },

    computed: {
      indexStart() {
        return this.itemsPerPage * (this.page - 1);
      },
      indexEnd() {
        return this.indexStart + this.itemsPerPage - 1;
      },

      ...mapGetters([
        'itemsPerPage',
        'pages',
      ]),
      ...mapState([
        'page',
      ]),
    },

    props: {
      albums: Array,
      required: true,
    }
  }
</script>
