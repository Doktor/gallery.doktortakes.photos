<template>
  <div v-if="!loading">
    <header class="manage-album-header">
      <AlbumCover :count="0" :album="album" :showManage="false" />
    </header>

    <main class="manage-album-container">
      <div class="manage-album-details">
        <AlbumForm
          v-if="!loading"
          :album="album"
          @save="saveAlbum"
          :isUpdate="true"
          :licenseOptions="licenseOptions"
        />

        <CustomButton
          class="button-danger"
          @click="showDeleteAlbumModal = true"
        >
          Delete album
        </CustomButton>

        <template v-if="album.parent || album.children.length > 0">
          <h2>Related albums</h2>

          <router-link
            v-if="album.parent !== null"
            :to="{
              name: 'editAlbum',
              params: { path: album.parent.split('/') },
            }"
          >
            Edit parent album
          </router-link>

          <AlbumChildrenListTiles :album="album" :route="'editAlbum'" />
        </template>
      </div>

      <PhotoManager
        class="manage-album-photos"
        :album="album"
        :photos="filteredPhotos"
        :showPhotosInChildAlbums="showPhotosInChildAlbums"
        @addPhoto="addPhoto"
        @removePhotosByHash="removePhotosByHash"
        @toggleShowPhotosInChildAlbums="toggleShowPhotosInChildAlbums"
        @setAlbum="setAlbum"
      />
    </main>

    <DeleteAlbumModal
      v-show="showDeleteAlbumModal"
      :album="album"
      @close="showDeleteAlbumModal = false"
      @submit="deleteAlbum"
    />
  </div>
</template>

<script>
import AlbumChildrenListTiles from "@/components/albumDetail/AlbumChildrenListTiles";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import DeleteAlbumModal from "./DeleteAlbumModal";
import PhotoManager from "./PhotoManager";
import PhotoUploader from "./PhotoUploader";
import { mapState } from "vuex";
import { editorTitleTemplate } from "@/store/mutations";
import { AlbumService } from "@/services/AlbumService";
import { ManageAlbumService } from "@/services/manage/ManageAlbumService";
import CustomButton from "@/components/form/CustomButton";
import AlbumCover from "@/pages/public/AlbumDetailPage/AlbumCover.vue";
import AlbumForm from "@/components/manage/AlbumForm.vue";
import { ManageLicenseService } from "@/services/manage/ManageLicenseService";

export default {
  components: {
    AlbumForm,
    AlbumCover,
    CustomButton,
    AlbumChildrenListTiles,
    DeleteAlbumModal,
    FixedWidthContainer,
    PhotoManager,
    PhotoUploader,
  },

  data() {
    return {
      album: {},
      photos: [],

      licenses: [],

      showPhotosInChildAlbums: false,
      allPhotos: null,

      showDeleteAlbumModal: false,
    };
  },

  computed: {
    ...mapState(["loading"]),

    routePath() {
      return this.$route.params.path;
    },

    filteredPhotos() {
      return this.showPhotosInChildAlbums ? this.allPhotos : this.photos;
    },

    licenseOptions() {
      return this.licenses.map((license) => {
        return {
          value: license.id,
          display: license.displayName,
        };
      });
    },

    breadcrumbs() {
      return [
        { label: "Manage", to: { name: "manage" } },
        {
          label: this.album.name,
          to: { name: "editAlbum", params: { path: this.routePath } },
        },
      ];
    },
  },

  async created() {
    this.$store.commit("setLoading", true);

    await this.loadAlbum();
    await this.loadLicenses();

    this.$store.commit("setLoading", false);
  },

  methods: {
    addPhoto(photo) {
      this.photos.push(photo);
    },

    removePhotosByHash(hashes) {
      for (let hash of hashes) {
        let index = this.photos.findIndex((photo) => photo.md5 === hash);

        if (index === -1) {
          continue;
        }

        this.photos.splice(index, 1);
      }
    },

    setAlbum(newAlbum) {
      let oldAlbum = this.album;

      if (oldAlbum.name !== newAlbum.name) {
        document.title = editorTitleTemplate.format(newAlbum.name);
      }

      // Prevent duplicate navigation
      if (oldAlbum.path !== undefined && oldAlbum.path !== newAlbum.path) {
        let resolved = this.$router.resolve({
          name: "editAlbum",
          params: { path: newAlbum.path.split("/") },
        });

        // Use history.replaceState instead of $router.replace to prevent
        // the component from reloading
        window.history.replaceState(null, null, resolved.href);
      }

      this.album = newAlbum;
    },

    async toggleShowPhotosInChildAlbums() {
      if (this.allPhotos === null) {
        let { content } = await ManageAlbumService.listAllPhotos(
          this.routePath,
        );
        this.allPhotos = content.photos;
      }

      this.showPhotosInChildAlbums = !this.showPhotosInChildAlbums;
    },

    async loadAlbum() {
      let { ok, album, photos } = await AlbumService.getAlbum({
        rawPath: this.routePath,
        code: "",
      });

      if (!ok) {
        this.$store.commit("addNotification", {
          message: "Album not found.",
          status: "error",
        });
        await this.$router.push({ name: "index" });

        return;
      }

      this.setAlbum(album);
      this.photos = photos;
    },

    async loadLicenses() {
      this.licenses = await ManageLicenseService.listLicenses();
    },

    async saveAlbum(album) {
      let newAlbum = await ManageAlbumService.saveAlbum(album);
      this.setAlbum(newAlbum);
    },

    async deleteAlbum() {
      await ManageAlbumService.deleteAlbum(this.album.path);
    },
  },

  watch: {
    async routePath() {
      await this.loadAlbum();
    },

    breadcrumbs(val) {
      this.$store.commit("setBreadcrumbs", val);
    },
  },
};
</script>

<style lang="scss" scoped>
body {
  max-width: 1100px;
  margin-bottom: 3rem;
}

section {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

h2 {
  margin: 0.5rem 0;
}

$breakpoint: 1201px;
$margin: 32px;

.manage-album-header {
  margin-bottom: $margin;
}

.manage-album-container {
  display: flex;
  justify-content: flex-start;
  flex-direction: column;

  @media (min-width: $breakpoint) {
    flex-direction: row;
  }
}

.manage-album-details {
  @media (min-width: $breakpoint) {
    min-width: 480px;
    margin-right: $margin;
  }
}

.manage-album-photos {
  width: 100%;
}

.photo-actions {
  display: flex;
  justify-content: space-between;
}
</style>
