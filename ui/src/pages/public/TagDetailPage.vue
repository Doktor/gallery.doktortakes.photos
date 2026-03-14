<template>
  <section v-if="!loading && tag !== null">
    <h2>#{{ tag.slug }}</h2>
    <AlbumGallery :albums="albums" :loading="false" />
  </section>
</template>

<script>
import { mapState } from "vuex";
import { baseTitle } from "@/router";
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
    ...mapState(["loading"]),

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
      this.$store.commit("setBreadcrumbs", val);
    },
  },

  async created() {
    document.title = "Tag: #{0} | {1}".format(this.slug, baseTitle);

    this.$store.commit("setLoading", true);

    this.tag = await TagService.getTag(this.slug);

    let albums = await AlbumService.getAllAlbums(true);
    this.albums = albums.filter((album) => album.tags.includes(this.tag.slug));

    this.$store.commit("setLoading", false);
  },
};
</script>
