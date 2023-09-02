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
      <CustomButton class="button-danger" @click="deleteAlbum">
        Delete
      </CustomButton>
    </div>
  </section>
</template>

<script>
import CustomButton from "@/components/form/CustomButton";

export default {
  components: { CustomButton },
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
        this.$store.commit("addNotification", {
          message: "Incorrect album name.",
          status: "error",
        });
      }
    },
  },
};
</script>
