<template>
  <section class="manage-photos">
    <h2>Manage photos</h2>

    <div>
      {{ photos.length }} photos in album,
      {{ selectedPhotoHashes.length }} photo{{
        selectedPhotoHashes.length | pluralize
      }}
      selected
    </div>

    <div class="actions">
      <div class="action-row">
        <CustomButton @click="toggleSelecting">
          {{ toggleSelectButtonText }}
        </CustomButton>
      </div>

      <template v-if="isSelecting">
        <div class="action-row">
          <CustomButton @click="selectAll">Select all</CustomButton>
          <CustomButton @click="selectNone">Select none</CustomButton>
          <CustomButton @click="selectInvert">Invert selection</CustomButton>
        </div>

        <div class="action-row">
          <CustomButton @click="setAlbumCover">Set cover</CustomButton>
          <CustomButton @click="deleteSelected">Delete</CustomButton>
        </div>
      </template>
    </div>

    <p v-if="!photos.length">This album does not contain any photos.</p>
    <Photos
      v-else
      :photos="photos"
      routeName="editPhoto"
      :selectedPhotoHashes="selectedPhotoHashes"
      :allowSelect="isSelecting"
      @select="select"
    />
  </section>
</template>

<script>
import Photos from "@/components/photoList/Photos.vue";
import { getCsrfToken, sendRequest } from "@/utils";
import { endpoints } from "@/constants";
import { ManageAlbumService } from "@/services/manage/ManageAlbumService";
import CustomButton from "@/components/form/CustomButton";

export default {
  components: {
    CustomButton,
    Photos,
  },

  props: {
    album: {
      type: Object,
      required: true,
    },
    photos: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      isSelecting: false,
      selectedPhotoHashes: [],
    };
  },

  computed: {
    hashes() {
      return this.photos.map((photo) => photo.md5);
    },
    toggleSelectButtonText() {
      return `${this.isSelecting ? "Disable" : "Enable"} selection mode`;
    },
  },

  filters: {
    pluralize(value) {
      return value === 1 ? "" : "s";
    },
  },

  methods: {
    async setAlbumCover() {
      if (this.selectedPhotoHashes.length !== 1) {
        return;
      }

      let selectedHash = this.selectedPhotoHashes[0];
      let currentHash = this.album.cover?.md5;

      if (currentHash !== null && selectedHash === currentHash) {
        this.$store.commit("addNotification", {
          message: "That photo is already set as the cover photo.",
          status: "error",
        });
        return;
      }

      let id = this.$store.commit("addNotification", {
        message: "Setting cover photo.",
        status: "default",
      });

      let { ok } = await sendRequest(
        endpoints.albumDetail.replace(":path", this.album.path),
        {
          method: "PATCH",
          body: JSON.stringify({ cover: selectedHash }),
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
        }
      );

      if (!ok) {
        this.$store.commit("addNotification", {
          message: "An error occurred when setting the cover photo.",
          status: "error",
        });
        return;
      }

      this.$store.commit("removeNotification", id);
      this.$store.commit("addNotification", {
        message: "Cover photo set successfully.",
        status: "success",
      });
      this.$emit("update");
    },

    toggleSelecting() {
      this.isSelecting = !this.isSelecting;
    },

    select(md5) {
      if (this.selectedPhotoHashes.includes(md5)) {
        this.selectedPhotoHashes.splice(
          this.selectedPhotoHashes.indexOf(md5),
          1
        );
      } else {
        this.selectedPhotoHashes.push(md5);
      }
    },

    selectAll() {
      this.selectedPhotoHashes = [...this.hashes];
    },
    selectInvert() {
      let hashes = [...this.hashes];
      let existingHashes = this.selectedPhotoHashes;

      for (let md5 of existingHashes) {
        hashes.remove(md5);
      }

      this.selectedPhotoHashes = hashes;
    },
    selectNone() {
      this.selectedPhotoHashes = [];
    },

    async deleteSelected() {
      let { ok } = await ManageAlbumService.deletePhotos(
        this.album.path,
        this.selectedPhotoHashes
      );

      if (ok) {
        this.selectedPhotoHashes = [];

        this.$emit("update");
      }
    },
  },
};
</script>

<style lang="scss">
.action-row {
  margin-bottom: 8px;

  .button + .button {
    margin-left: 8px;
  }
}
</style>
