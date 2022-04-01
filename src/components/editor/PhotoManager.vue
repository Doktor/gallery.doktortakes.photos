<template>
  <section class="manage-photos">
    <h2>Manage photos</h2>

    <div>
      {{ photos.length }} photos in album, {{ selectedPhotoHashes.length }} photo{{
        selectedPhotoHashes.length | pluralize
      }}
      selected
    </div>

    <div>
      <button @click="toggleSelecting">{{ toggleSelectButtonText }}</button>

      <template v-if="isSelecting">
        <div>
          <button @click="selectAll" type="button">Select all</button>
          <button @click="selectNone" type="button">Select none</button>
          <button @click="selectInvert" type="button">Invert selection</button>
        </div>

        <div>
          <button @click="setAlbumCover" type="button">Set cover</button>
          <button @click="deleteSelected" type="button">Delete</button>
        </div>
      </template>
    </div>

    <p v-if="!photos.length">This album does not contain any photos.</p>
    <Photos
      v-else
      :photos="photos"
      route="editPhoto"
      :selectedPhotoHashes="selectedPhotoHashes"
      :allowSelect="isSelecting"
      @select="select"
    />
  </section>
</template>

<script>
import Photos from "@/components/photoList/Photos.vue";
import { mapActions } from "vuex";
import { sendRequest } from "@/store/utils";
import { endpoints, getCsrfToken } from "@/store";

export default {
  components: {
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
      return `${this.isSelecting ? "Disable" : "Enable"} selection mode`
    },
  },

  filters: {
    pluralize(value) {
      return value === 1 ? "" : "s";
    },
  },

  methods: {
    ...mapActions(["setAlbumCover"]),

    toggleSelecting() {
      this.isSelecting = !this.isSelecting;
    },

    select(md5) {
      if (this.selectedPhotoHashes.includes(md5)) {
        this.selectedPhotoHashes.splice(this.selectedPhotoHashes.indexOf(md5), 1);
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
      let { ok } = await sendRequest(
        endpoints.albumPhotoList.replace(":path", this.album.path),
        {
          method: "DELETE",
          body: JSON.stringify({
            photos: this.selectedPhotoHashes,
          }),
          headers: {
            "Content-Type": "application/json; charset=utf-8",
            "X-CSRFToken": getCsrfToken(),
          },
        },
      );

      if (ok) {
        this.selectedPhotoHashes = [];

        this.$emit('update')
      }
    },
  },
};
</script>
