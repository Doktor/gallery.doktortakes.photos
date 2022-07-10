<template>
  <FixedWidthContainer>
    <router-link :to="{ name: 'manage' }">Back to editor</router-link>

    <template v-if="!loading">
      <header>
        <h2 id="album-name">{{ album.name }}</h2>
        <AlbumLinks :album="album" />
      </header>

      <h2>Album details</h2>
      <AlbumDetails v-if="!loading" :album="album" @save="saveAlbum" />

      <template v-if="album.parent || album.children.length > 0">
        <h2>Related albums</h2>

        <router-link
          v-if="album.parent !== null"
          :to="{ name: 'editAlbum', params: { path: album.parent.split('/') } }"
        >
          Edit parent album
        </router-link>

        <AlbumChildren :album="album" :route="'editAlbum'" />
      </template>

      <PhotoUploader :path="album.path" />
      <PhotoManager :album="album" :photos="photos" @update="loadAlbum" />

      <DeleteAlbumForm :album="album" @delete="deleteAlbum" />
    </template>
  </FixedWidthContainer>
</template>

<script>
import AlbumChildren from "@/components/albumList/AlbumChildren";
import AlbumDetails from "@/components/editor/AlbumDetails.vue";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import DeleteAlbumForm from "@/components/editor/DeleteAlbumForm.vue";
import PhotoManager from "@/components/editor/PhotoManager.vue";
import PhotoUploader from "@/components/editor/PhotoUploader.vue";
import { mapState } from "vuex";
import { router } from "@/router/main";
import { editorTitleTemplate } from "@/store/mutations";
import AlbumLinks from "@/components/editor/AlbumLinks";
import { AlbumService } from "@/services/AlbumService";
import { ManageAlbumService } from "@/services/manage/ManageAlbumService";

export default {
  components: {
    AlbumLinks,
    AlbumChildren,
    AlbumDetails,
    DeleteAlbumForm,
    FixedWidthContainer,
    PhotoManager,
    PhotoUploader,
  },

  data() {
    return {
      album: {},
      photos: [],
    };
  },

  computed: {
    ...mapState(["loading"]),

    routePath() {
      return this.$route.params.path;
    },
  },

  async created() {
    await this.loadAlbum();
  },

  methods: {
    async loadAlbum() {
      this.$store.commit("setLoading", true);

      let { ok, album, photos } = await AlbumService.getAlbum({
        rawPath: this.routePath,
        code: "",
      });

      if (!ok) {
        this.$store.commit("addNotification", "Album not found.");
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

#album-form-save {
  align-self: flex-end;
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

.delete-album {
  display: flex;
  max-width: 600px;
}
</style>
