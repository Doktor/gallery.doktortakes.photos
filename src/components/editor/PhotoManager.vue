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
      <button @click="selectAll" type="button">Select all</button>
      <button @click="selectNone" type="button">Select none</button>
      <button @click="selectInvert" type="button">Invert selection</button>
    </div>

    <div class="photo-actions">
      <div>
        <button @click="setAlbumCover">Set cover</button>
      </div>

      <div>
        <button @click="deleteSelected" type="button">Delete</button>
      </div>
    </div>

    <p v-if="!photos.length">This album does not contain any photos.</p>
    <Photos
      v-else
      :photos="photos"
      :selectedPhotoHashes="selectedPhotoHashes"
      :allowSelect="true"
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
      selectedPhotoHashes: [],
    };
  },

  computed: {
    hashes() {
      return this.photos.map((photo) => photo.md5);
    },
  },

  filters: {
    pluralize(value) {
      return value === 1 ? "" : "s";
    },
  },

  methods: {
    ...mapActions(["setAlbumCover"]),

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
