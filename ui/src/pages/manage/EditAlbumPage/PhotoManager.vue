<template>
  <div style="text-align: left">
    <div>
      {{ photos.length }} photos in album,
      {{ selectedPhotoHashes.length }} photo{{
        pluralize(selectedPhotoHashes.length)
      }}
      selected
    </div>

    <div>
      <CustomInput
        type="checkbox"
        label="Show photos in child albums"
        v-model="showPhotosInChildAlbumsComputed"
      />
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

    <PhotoUploader :path="album.path" @addPhoto="addPhoto" />

    <p v-if="!photos.length">This album does not contain any photos.</p>
    <PhotoGallery
      v-else
      :photos="photos"
      routeName="editPhoto"
      :selectedPhotoHashes="selectedPhotoHashes"
      :allowSelect="isSelecting"
      @select="select"
    />
  </div>
</template>

<script>
import PhotoGallery from "@/components/photoList/PhotoGallery";
import { ManageAlbumService } from "@/services/manage/ManageAlbumService";
import CustomButton from "@/components/form/CustomButton";
import CustomInput from "@/components/form/CustomInput";
import FixedWidthContainer from "@/components/FixedWidthContainer.vue";
import PhotoUploader from "@/pages/manage/EditAlbumPage/PhotoUploader.vue";
import { pluralize } from "@/utils";

export default {
  components: {
    PhotoUploader,
    FixedWidthContainer,
    CustomInput,
    CustomButton,
    PhotoGallery,
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

    showPhotosInChildAlbums: {
      type: Boolean,
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

    showPhotosInChildAlbumsComputed: {
      get() {
        return this.showPhotosInChildAlbums;
      },
      set() {
        this.$emit("toggleShowPhotosInChildAlbums");
      },
    },
  },

  methods: {
    pluralize,

    addPhoto(photo) {
      this.$emit("addPhoto", photo);
    },

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

      let album = await ManageAlbumService.setAlbumCover(
        this.album,
        selectedHash,
      );
      this.$emit("setAlbum", album);
    },

    toggleSelecting() {
      this.isSelecting = !this.isSelecting;
    },

    select(md5) {
      if (this.selectedPhotoHashes.includes(md5)) {
        this.selectedPhotoHashes.splice(
          this.selectedPhotoHashes.indexOf(md5),
          1,
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
        this.selectedPhotoHashes,
      );

      if (ok) {
        this.$emit("removePhotosByHash", [...this.selectedPhotoHashes]);

        this.selectedPhotoHashes = [];
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
