<template>
  <ul class="album-list-dc-items">
    <AlbumDetailedCard
        v-for="(album, index) in albums"
        :album="album"
        :isLoaded="album.isLoaded"
        :isVisible="indexStart <= index && index <= indexEnd"
        :key="album.path"
        :route="route"
    />
  </ul>
</template>

<script>
  import AlbumDetailedCard from "./AlbumDetailedCard.vue";


  export default {
    components: {
      AlbumDetailedCard,
    },

    name: "AlbumListDetailedCards",

    props: {
      albums: {
        type: Array,
        required: true,
      },
      route: {
        type: String,
        default: "album",
      },

      indexStart: {
        type: Number,
      },
      indexEnd: {
        type: Number,
      },
    },
  }
</script>
