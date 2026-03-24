<template>
  <Modal @close="$emit('close')">
    <div>
      <h3>Delete album</h3>

      <p>
        Recursively delete this album and all of the albums and photos contained
        within. <b>This cannot be undone!</b>
        To continue, type the name of this album below:
        <b>{{ album.name }}</b>
      </p>

      <input v-model="name" title="Name" type="text" />
      <CustomButton class="button-danger" @click="deleteAlbum">
        Delete album
      </CustomButton>
    </div>
  </Modal>
</template>

<script>
import { useStore } from "@/store";
import CustomButton from "@/components/form/CustomButton";
import Modal from "@/components/Modal.vue";

export default {
  components: {
    Modal,
    CustomButton,
  },

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
        this.$emit("submit");
        return;
      }

      useStore().addNotification({
        message: "Incorrect album name.",
        status: "error",
      });
    },
  },
};
</script>
