<template>
  <FixedWidthContainer>
    <router-link :to="{ name: 'manage' }">Back to editor</router-link>
    <h2>Create new album</h2>
    <AlbumForm
      class="form--small"
      :album="album"
      :save-button-text="'Create album'"
      :update="false"
      @save="createAlbum"
    />
  </FixedWidthContainer>
</template>

<script>
import AlbumForm from "../../components/manage/AlbumForm.vue";
import FixedWidthContainer from "../../components/FixedWidthContainer.vue";
import { ManageAlbumService } from "../../services/manage/ManageAlbumService";

export default {
  components: {
    AlbumForm,
    FixedWidthContainer,
  },

  data() {
    return {
      album: {
        name: "",
        place: "",
        location: "",
        description: "",
        start: "",
        end: "",
        access_level: 0,
        access_code: "",
        parent: "",
        users: [],
        groups: [],
        tags: [],
      },
    };
  },

  methods: {
    async createAlbum(album) {
      await ManageAlbumService.createAlbum(album);
    },
  },
};
</script>
