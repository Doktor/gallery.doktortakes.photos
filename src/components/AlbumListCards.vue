<template>
  <div>
    <AlbumCard
        v-for="(album, index) in albums"
        :album="album"
        :isLoaded="album.isLoaded"
        :isVisible="indexStart <= index && index <= indexEnd"
        :key="album.path"
        :route="route"
    />
  </div>
</template>

<script>
  import AlbumCard from "./AlbumCard.vue";


  export default {
    components: {
      AlbumCard,
    },

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
        required: true,
      },
      indexEnd: {
        type: Number,
        required: true,
      },
    },
  }
</script>
