<template>
  <FixedWidthContainer>
    <div>
      <router-link :to="{ name: 'manage' }">Return to dashboard</router-link>
    </div>

    <div>
      <router-link
        :to="{
          name: 'editAlbum',
          params: { path: this.$route.params.path },
        }"
        >Return to album</router-link
      >
    </div>

    <template v-if="!loading">
      <header>
        <h2 class="album-name">{{ album.name }}</h2>
        <h3 class="photo-hash">{{ photo.md5 }}</h3>
      </header>

      <section class="taxa-table">
        <h2>Manage taxa</h2>
        <PhotoTaxaTable :photo="photo" />
      </section>

      <main>
        <section class="photo-details">
          <div>
            <h2>Metadata</h2>
            <PhotoMetadataTable class="photo-details-table" :photo="photo" />
          </div>

          <div>
            <h2>EXIF</h2>
            <PhotoExifTable class="photo-details-table" :photo="photo" />
          </div>
        </section>

        <section class="image-container">
          <img
            class="image-preview"
            :src="photo.images.display?.url ?? photo.images.original.url"
          />
        </section>
      </main>

      <section>
        <h2>Thumbnails</h2>
        <PhotoThumbnailsTable
          class="photo-details-table"
          :thumbnails="thumbnails"
        />
      </section>

      <section>
        <h2>Create thumbnail</h2>

        <ThumbnailForm :photo="photo" @update="loadThumbnails" />
      </section>
    </template>
  </FixedWidthContainer>
</template>

<script>
import FixedWidthContainer from "@/components/FixedWidthContainer";
import { mapState } from "vuex";
import { AlbumService } from "@/services/AlbumService";
import { PhotoService } from "@/services/PhotoService";
import PhotoMetadataTable from "./PhotoMetadataTable";
import PhotoExifTable from "./PhotoExifTable";
import PhotoThumbnailsTable from "./PhotoThumbnailsTable";
import ThumbnailForm from "./ThumbnailForm";
import { ManagePhotoService } from "@/services/manage/ManagePhotoService";
import PhotoTaxaTable from "@/pages/manage/EditPhotoPage/PhotoTaxaTable.vue";

export default {
  components: {
    PhotoTaxaTable,
    ThumbnailForm,
    PhotoThumbnailsTable,
    PhotoExifTable,
    PhotoMetadataTable,
    FixedWidthContainer,
  },

  data() {
    return {
      album: {},
      photo: {},
      thumbnails: [],
    };
  },

  computed: {
    ...mapState(["loading"]),

    routePath() {
      return this.$route.params.path;
    },
    routeMd5() {
      return this.$route.params.md5;
    },
  },

  async created() {
    this.$store.commit("setLoading", true);

    await Promise.all([
      this.loadAlbum(),
      this.loadPhoto(),
      this.loadThumbnails(),
    ]);

    this.$store.commit("setLoading", false);
  },

  methods: {
    async loadAlbum() {
      let { ok, album } = await AlbumService.getAlbum({
        rawPath: this.routePath,
        code: "",
        getPhotos: false,
      });

      if (!ok) {
        this.$store.commit("addNotification", {
          message: "Album not found.",
          status: "error",
        });
        await this.$router.push({ name: "albums" });
        return;
      }

      this.album = album;
    },

    async loadPhoto() {
      let { ok, content } = await PhotoService.get(this.routeMd5);

      if (!ok) {
        this.$store.commit("addNotification", {
          message: "Photo not found.",
          status: "error",
        });
        await this.$router.push({ name: "albums" });
        return;
      }

      this.photo = content;
    },

    async loadThumbnails() {
      let { ok, content } = await ManagePhotoService.getThumbnails(
        this.routeMd5,
      );

      if (!ok) {
        this.$store.commit("addNotification", {
          message: "Photo not found.",
          status: "error",
        });
        await this.$router.push({ name: "albums" });
        return;
      }

      this.thumbnails = content;
    },
  },

  watch: {
    async routePath() {
      await this.loadAlbum();
    },
  },
};
</script>

<style lang="scss" scoped>
main {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
}

h2,
h3 {
  margin: 0;
}

.photo-hash {
  @include text-font();
}

.photo-details {
  margin-right: 16px;
}

.photo-details,
.image-container {
  width: 50%;
}

.taxa-table {
  width: 100%;
}

.photo-details-table {
  width: 100%;
}

.image-preview {
  width: 100%;
}
</style>
