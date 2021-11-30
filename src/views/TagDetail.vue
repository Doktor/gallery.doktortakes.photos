<template>
  <section v-if="!loading && tag !== null">
    <h2>#{{ tag.slug }}</h2>
    <SearchAlbums :albums="albums" :loading="false" />
  </section>
</template>

<script>
  import {mapState} from 'vuex';
  import {baseTitle} from "@/router/main.js";
  import SearchAlbums from "@/components/albumList/SearchAlbums";
  import {AlbumService} from "@/services/AlbumService";


  export default {
    components: {
      SearchAlbums,
    },

    data() {
      return {
        albums: [],
        tag: {},
      }
    },

    computed: {
      ...mapState([
        'loading',
      ]),

      route() {
        return this.$route;
      },

      slug() {
        return this.$route.params.slug;
      },
    },

    async created() {
      document.title = "Tag: #{0} | {1}".format(this.slug, baseTitle);

      this.tag = await this.$store.dispatch('getTag', this.slug);

      this.$store.commit('setLoading', true);

      let albums = await AlbumService.getAllAlbums(true);
      this.albums = albums.filter(album => album.tags.includes(this.tag.slug));

      this.$store.commit('setLoading', false);
    },
  }
</script>
