<template>
  <ul class="album-list-dc-items">
    <AlbumDetailedCard
        v-for="album in albums"
        :album="album"
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
    },
  }
</script>
