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
  import AlbumCard from "./AlbumCard";


  export default {
    components: {
      AlbumCard,
    },

    props: {
      album: {
        type: Object,
        required: true,
      },
      route: {
        type: String,
        default: 'album',
      },
    },
  }
</script>
