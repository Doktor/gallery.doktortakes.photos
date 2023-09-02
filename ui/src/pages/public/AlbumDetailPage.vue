<template>
  <div>
    <section class="album-cover-container">
      <AlbumCover
        :album="album"
        :count="photos.length"
        :isSkeleton="!!loading"
      />
    </section>

    <AlbumChildrenListTiles v-if="!loading" :album="album" />

    <PhotoGallery
      v-if="loading"
      :photos="new Array(12).fill({})"
      :allowSelect="false"
      :isLoading="true"
    />
    <PhotoGallery
      v-else-if="photos.length > 0"
      :photos="photos"
      :allowSelect="false"
    />

    <div
      class="album-empty-text"
      v-if="photos.length === 0 && album.children?.length === 0"
    >
      There are no photos in this album.
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import AlbumTile from "../../components/albumTile/AlbumTile.vue";
import AlbumChildrenListTiles from "../../components/albumDetail/AlbumChildrenListTiles.vue";
import AlbumCover from "../../components/albumDetail/AlbumCover.vue";
import PhotoGallery from "../../components/photoList/PhotoGallery.vue";
import { titleTemplate } from "../../store/mutations";
import { AlbumService } from "../../services/AlbumService";

export default {
  components: {
    AlbumTile,
    AlbumChildrenListTiles,
    AlbumCover,
    PhotoGallery,
  },

  data() {
    return {
      album: {},
      photos: [],
    };
  },

  computed: {
    ...mapState(["loading"]),

    routeAccessCode() {
      return this.$route.query.code || "";
    },

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
        code: this.routeAccessCode,
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

      document.title = titleTemplate.format(album.name);
      this.$store.commit("setLoading", false);
    },
  },

  watch: {
    async routePath() {
      await this.loadAlbum();
    },
  },
};
</script>

<style scoped>
.album-cover-container {
  margin: 0;
}

.album-empty-text {
  margin-top: 3rem;
}
</style>
