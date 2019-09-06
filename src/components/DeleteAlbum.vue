<template>
  <section id="delete-album">
    <h2>Delete album</h2>

    <p>
      Deletes this album and all descendant albums and photos.
      <strong>This cannot be undone!</strong><br>
      To confirm deletion, enter the name of the album, case-sensitive.
    </p>

    <div class="delete-album">
      <input ref="albumName" title="Name" type="text">
      <button
          type="button"
          @click="deleteAlbum"
      >Delete
      </button>
    </div>
  </section>
</template>

<script>
  export default {
    methods: {
      deleteAlbum() {
        if (this.$refs.albumName.value === this.$store.state.album.name) {
          this.$store.dispatch('deleteAlbum');
        }
      },
    },
  }
</script>
