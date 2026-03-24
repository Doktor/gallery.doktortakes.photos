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
      :isLoading="loading"
      :photos="photos"
      :allowSelect="false"
      :routeName="isExternal ? 'externalPhoto' : 'photo'"
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
import { mapState } from "pinia";
import { useStore } from "@/store";

import AlbumTile from "@/components/albumTile/AlbumTile";
import AlbumChildrenListTiles from "@/components/albumDetail/AlbumChildrenListTiles";
import AlbumCover from "./AlbumCover";
import PhotoGallery from "@/components/photoList/PhotoGallery";
import { AlbumService } from "@/services/AlbumService";

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

  props: {
    isExternal: {
      type: Boolean,
      default: false,
    },
  },

  computed: {
    ...mapState(useStore, ["loading"]),

    routeAccessCode() {
      return this.$route.query.code || "";
    },

    routePath() {
      return this.$route.params.pathArray;
    },

    breadcrumbs() {
      if (!this.album.name) {
        return [];
      }

      return [
        this.isExternal
          ? {
              label: "Appearances",
              to: { name: "externalAlbums" },
            }
          : {
              label: "Albums",
              to: { name: "index" },
            },
        ...this.album.hierarchy.map((album) => {
          return {
            label: album.name,
            to: {
              name: this.isExternal ? "externalAlbum" : "album",
              params: { pathArray: album.path.split("/") },
            },
          };
        }),
      ];
    },
  },

  async created() {
    await this.loadAlbum();
  },

  methods: {
    async loadAlbum() {
      const store = useStore();
      store.setLoading(true);

      let { ok, album, photos } = await AlbumService.getAlbum({
        rawPath: this.routePath,
        code: this.routeAccessCode,
      });

      if (!ok) {
        store.addNotification({
          message: "Album not found.",
          status: "error",
        });
        await this.$router.push({ name: "index" });

        return;
      }

      this.album = album;
      this.photos = photos;

      store.setTitle(album.name);
      store.setLoading(false);
    },
  },

  watch: {
    breadcrumbs(val) {
      useStore().setBreadcrumbs(val);
    },

    async routePath(newPath, oldPath) {
      if (oldPath.join("/") === newPath.join("/")) {
        return;
      }

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
