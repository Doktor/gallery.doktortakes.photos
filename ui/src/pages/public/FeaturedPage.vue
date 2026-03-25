<template>
  <div v-if="album.name">
    <h2 class="gallery-title">
      <template v-if="album.parent">
        {{ album.parent }} // {{ album.name }}
      </template>
      <template v-else>{{ album.name }}</template>
    </h2>

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
    async routePath(newPath, oldPath) {
      if (newPath === oldPath) {
        return;
      }

      await this.loadAlbum();
    },
  },
};
</script>

<style lang="scss" scoped>
@use "@/styles/variables";

.gallery-title {
  @include variables.headings-font();
  font-size: 2.5rem;
  text-align: left;
  text-transform: uppercase;
  overflow-wrap: break-word;

  width: 100%;
  margin-bottom: variables.$item-spacing;
}
</style>
