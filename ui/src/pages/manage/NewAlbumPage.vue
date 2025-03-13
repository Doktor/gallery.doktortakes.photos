<template>
  <FixedWidthContainer>
    <h2>Create new album</h2>

    <AlbumForm
      class="form--small"
      :album="album"
      :save-button-text="'Create album'"
      :update="false"
      @save="createAlbum"
      :licenseOptions="licenseOptions"
    />
  </FixedWidthContainer>
</template>

<script>
import AlbumForm from "@/components/manage/AlbumForm";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import { ManageAlbumService } from "@/services/manage/ManageAlbumService";
import { ManageLicenseService } from "@/services/manage/ManageLicenseService";

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
        accessLevel: 0,
        accessCode: "",
        parent: "",
        users: [],
        groups: [],
        tags: [],
      },

      licenseOptions: [],
    };
  },

  async created() {
    this.$store.commit("setLoading", true);

    await this.loadLicenses();

    this.$store.commit("setLoading", false);
  },

  methods: {
    async createAlbum(album) {
      await ManageAlbumService.createAlbum(album);
    },

    async loadLicenses() {
      let licenses = await ManageLicenseService.listLicenses();

      this.licenseOptions = licenses.map((license) => {
        return {
          value: license.id,
          display: license.displayName,
        };
      });
    },
  },
};
</script>
