<template>
  <section v-if="album.children.length > 0" class="albums">
    <AlbumCard
        v-for="childAlbum in album.children"
        :album="childAlbum"
        :is-loaded="true"
        :is-visible="true"
        :key="childAlbum.path"
        :route="route"
    />
  </section>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumCard from "./AlbumCard.vue";


  export default {
    components: {
      AlbumCard,
    },

    computed: {
      ...mapState([
        'album',
      ]),
    },

    props: {
      route: {
        type: String,
      },
    },
  }
</script>
