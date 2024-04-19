<template>
  <FixedWidthContainer>
    <router-link :to="{ name: 'manage' }">Back to editor</router-link>

    <template v-if="!loading">
      <header>
        <h2 id="album-name">{{ album.name }}</h2>
        <AlbumLinks :album="album" />
      </header>

      <h2>Album details</h2>

      <div>
        <CustomButton
          class="button-danger"
          @click="showDeleteAlbumModal = true"
        >
          Delete album
        </CustomButton>
      </div>

      <AlbumDetails v-if="!loading" :album="album" @save="saveAlbum" />

      <template v-if="album.parent || album.children.length > 0">
        <h2>Related albums</h2>

        <router-link
          v-if="album.parent !== null"
          :to="{ name: 'editAlbum', params: { path: album.parent.split('/') } }"
        >
          Edit parent album
        </router-link>

        <AlbumChildrenListTiles :album="album" :route="'editAlbum'" />
      </template>

      <PhotoUploader :path="album.path" />
      <PhotoManager
        :album="album"
        :photos="filteredPhotos"
        :showPhotosInChildAlbums="showPhotosInChildAlbums"
        @toggleShowPhotosInChildAlbums="toggleShowPhotosInChildAlbums"
        @update="loadAlbum"
      />

      <DeleteAlbumModal
        v-show="showDeleteAlbumModal"
        :album="album"
        @close="showDeleteAlbumModal = false"
        @submit="deleteAlbum"
      />
    </template>
  </FixedWidthContainer>
</template>

<script>
import AlbumChildrenListTiles from "@/components/albumDetail/AlbumChildrenListTiles";
import AlbumDetails from "./AlbumDetails";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import DeleteAlbumModal from "./DeleteAlbumModal";
import PhotoManager from "./PhotoManager";
import PhotoUploader from "./PhotoUploader";
import { mapState } from "vuex";
import { router } from "@/router";
import { editorTitleTemplate } from "@/store/mutations";
import AlbumLinks from "@/components/manage/AlbumLinks";
import { AlbumService } from "@/services/AlbumService";
import { ManageAlbumService } from "@/services/manage/ManageAlbumService";
import CustomButton from "@/components/form/CustomButton";

export default {
  components: {
    CustomButton,
    AlbumLinks,
    AlbumChildrenListTiles,
    AlbumDetails,
    DeleteAlbumModal,
    FixedWidthContainer,
    PhotoManager,
    PhotoUploader,
  },

  data() {
    return {
      album: {},
      photos: [],

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
  },

  async created() {
    await this.loadAlbum();
  },

  methods: {
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
      this.$store.commit("setLoading", true);

      let { ok, album, photos } = await AlbumService.getAlbum({
        rawPath: this.routePath,
        code: "",
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
      this.photos = photos;

      this.updateDocumentTitle();
      this.$store.commit("setLoading", false);
    },

    async saveAlbum(album) {
      await ManageAlbumService.saveAlbum(album);
      this.updateDocumentTitle();
    },

    updateDocumentTitle() {
      let newTitle = editorTitleTemplate.format(this.album.name);

      // Update history entry
      if (document.title !== newTitle) {
        document.title = newTitle;

        let route = {
          name: "editAlbum",
          params: { path: this.album.path.split("/") },
        };
        let resolved = router.resolve(route);
        window.history.replaceState(null, newTitle, resolved.href);
      }
    },

    async deleteAlbum() {
      await ManageAlbumService.deleteAlbum(this.album.path);
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

.count {
  line-height: 1;
  margin: 1rem 0;
}

.manage-photos {
  margin: 1rem 0;
}

.photo-actions {
  display: flex;
  justify-content: space-between;
}
</style>
