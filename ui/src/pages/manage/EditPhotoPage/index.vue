<template>
  <FixedWidthContainer v-if="!loading" :width="1200">
    <section class="photo-details-section">
      <div>
        <h2>Photo details</h2>

        <PhotoDetailsForm :photo="photo" @update="loadPhoto" />
      </div>

      <div>
        <h2>Photo preview</h2>

        <a
          :href="thumbnailUrl"
          target="_blank"
          rel="noopener noreferrer nofollow"
        >
          <img class="photo-image" :src="thumbnailUrl" />
        </a>
      </div>
    </section>

    <section class="photo-details-section">
      <div>
        <h2>Metadata</h2>

        <PhotoMetadataTable class="photo-thumbnails-table" :photo="photo" />
      </div>

      <div>
        <h2>EXIF</h2>

        <PhotoExifTable class="photo-thumbnails-table" :photo="photo" />
      </div>
    </section>

    <section class="photo-details-section">
      <div>
        <h2>Thumbnails</h2>

        <PhotoThumbnailsTable
          class="photo-thumbnails-table"
          :thumbnails="thumbnails"
        />
      </div>

      <div>
        <h2>Create thumbnail</h2>

        <ThumbnailForm :photo="photo" @update="loadThumbnails" />
      </div>
    </section>

    <section class="photo-taxa-table">
      <h2>Manage taxa</h2>

      <PhotoTaxonTable :photo="photo" />
    </section>
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
import PhotoDetailsForm from "./PhotoDetailsForm";
import { ManagePhotoService } from "@/services/manage/ManagePhotoService";
import PhotoTaxonTable from "./PhotoTaxonTable";

export default {
  name: "EditPhotoPage",
  components: {
    PhotoTaxonTable,
    PhotoDetailsForm,
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
      return this.$route.params.pathArray;
    },
    routeMd5() {
      return this.$route.params.md5;
    },

    thumbnailUrl() {
      return this.photo.images.display?.url ?? this.photo.images.original.url;
    },

    pageTitle() {
      if (!this.photo.md5 || !this.album.name) {
        return null;
      }

      return "Editing " + this.photo.md5.substring(0, 8) + " | " + this.album.name;
    },

    breadcrumbs() {
      if (!this.album.name) {
        return [];
      }

      return [
        { label: "Manage", to: { name: "manage" } },
        {
          label: this.album.name,
          to: { name: "editAlbum", params: { pathArray: this.routePath } },
        },
        {
          label: this.photo.md5,
          to: {
            name: "editPhoto",
            params: { pathArray: this.routePath, md5: this.routeMd5 },
          },
        },
      ];
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
        await this.$router.push({ name: "index" });
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
        await this.$router.push({ name: "index" });
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
        await this.$router.push({ name: "index" });
        return;
      }

      this.thumbnails = content;
    },
  },

  watch: {
    async routePath() {
      await this.loadAlbum();
    },

    pageTitle(val) {
      this.$store.commit("setTitle", val);
    },

    breadcrumbs(val) {
      this.$store.commit("setBreadcrumbs", val);
    },
  },
};
</script>

<style lang="scss" scoped>
$margin: 24px;

section {
  margin: $margin 0;
}

.photo-hash {
  @include variables.text-font();
}

.photo-details-section {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  gap: $margin;

  & > div {
    width: 50%;
  }
}

.photo-image {
  width: 100%;
}
</style>
