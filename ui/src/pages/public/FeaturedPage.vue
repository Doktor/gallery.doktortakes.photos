<template>
  <div v-if="!loading">
    <PhotoGallery :photos="photos" :shouldPaginate="false" />
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useStore } from "@/store";
import { AlbumService } from "@/services/AlbumService";
import PhotoGallery from "@/components/photoList/PhotoGallery.vue";

export default {
  name: "FeaturedPage",

  components: {
    PhotoGallery,
  },

  data() {
    return {
      album: {},
      photos: [],
    };
  },

  computed: {
    ...mapState(useStore, ["loading"]),

    routePath() {
      return this.$route.params.pathArray;
    },

    breadcrumbs() {
      if (!this.album.name) {
        return [];
      }

      return [
        {
          label: "Featured",
        },
        ...this.album.hierarchy.map((album) => {
          return {
            label: album.name,
            to: {
              name: "featuredAlbum",
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
      });

      if (ok) {
        this.album = album;
        this.photos = photos.sort((a, b) => b.index - a.index);
        store.setTitle(album.name);
      }

      store.setLoading(false);
    },
  },

  watch: {
    breadcrumbs(val) {
      useStore().setBreadcrumbs(val);
    },

    async routePath(newPath, oldPath) {
      if (newPath === oldPath) {
        return;
      }

      await this.loadAlbum();
    },
  },
};
</script>
