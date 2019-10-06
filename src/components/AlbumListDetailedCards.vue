<template>
  <ul class="album-list-dc-items">
    <AlbumDetailedCard
        v-for="album in albums"
        :album="album"
        :key="album.path"
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
      albums: Array,
      required: true,
    },
  }
</script>
