<template>
  <section v-if="!loading && tag !== null">
    <h2>#{{ tag.slug }}</h2>
    <AlbumGallery :albums="albums" :loading="false" />
  </section>
</template>

<script>
import { mapState } from "pinia";
import { useStore } from "@/store";
import AlbumGallery from "@/components/albumList/AlbumGallery";
import { AlbumService } from "@/services/AlbumService";
import { TagService } from "@/services/TagService";

export default {
  components: {
    AlbumGallery,
  },

  data() {
    return {
      albums: [],
      tag: {},
    };
  },

  computed: {
    ...mapState(useStore, ["loading"]),

    route() {
      return this.$route;
    },

    slug() {
      return this.$route.params.slug;
    },

    breadcrumbs() {
      if (!this.tag?.slug) {
        return [];
      }

      return [
        { label: "Tags", to: { name: "tags" } },
        {
          label: `#${this.tag.slug}`,
          to: {
            name: "tag",
            params: { slug: this.tag.slug },
          },
        },
      ];
    },
  },

  watch: {
    breadcrumbs(val) {
      useStore().setBreadcrumbs(val);
    },
  },

  async created() {
    const store = useStore();
    store.setTitle("Tag: #" + this.slug);

    store.setLoading(true);

    this.tag = await TagService.getTag(this.slug);
    this.albums = await AlbumService.getAlbumsForTag(this.slug);

    store.setLoading(false);
  },
};
</script>
