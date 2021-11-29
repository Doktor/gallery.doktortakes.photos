<template>
  <section v-if="!loading && tag !== null">
    <h2>#{{ tag.slug }}</h2>
    <SearchAlbums />
  </section>
</template>

<script>
  import {mapState} from 'vuex';
  import {baseTitle} from "@/router/main.js";
  import SearchAlbums from "@/components/albumList/SearchAlbums";


  export default {
    components: {
      SearchAlbums,
    },

    data() {
      return {
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

      this.$store.dispatch('getAllAlbums').then(() => {
        this.$store.commit('setAlbumsByTag', this.slug);
      });
    },
  }
</script>
