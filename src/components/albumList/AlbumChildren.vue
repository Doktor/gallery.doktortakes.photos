<template>
  <section v-if="album.children.length > 0" class="albums">
    <AlbumCard
      v-for="child in album.children"
      :album="child"
      :isLoaded="true"
      :isVisible="true"
      :key="child.path"
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
        default: 'album',
      },
    },
  }
</script>
