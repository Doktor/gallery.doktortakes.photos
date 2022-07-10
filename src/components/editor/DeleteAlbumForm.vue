<template>
  <section id="delete-album">
    <h2>Delete album</h2>

    <p>
      Deletes this album and all descendant albums and photos.
      <strong>This cannot be undone!</strong><br />
      To confirm deletion, enter the name of the album, case-sensitive.
    </p>

    <div class="delete-album">
      <input v-model="name" title="Name" type="text" />
      <button type="button" @click="deleteAlbum">Delete</button>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      name: "",
    };
  },
  methods: {
    deleteAlbum() {
      if (this.name === this.album.name) {
        this.$emit("delete");
      } else {
        this.$store.commit("addNotification", "Incorrect album name.");
      }
    },
  },
};
</script>
