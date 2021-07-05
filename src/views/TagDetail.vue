<template>
  <section v-if="!loading && tag !== null">
    <h2>#{{ tag.slug }}</h2>

    <div class="count">
      {{ results.length }} album{{ results.length|pluralize}}
    </div>

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

    computed: {
      ...mapState([
        'loading',
        'results',
        'tag',
      ]),

      route() {
        return this.$route;
      },

      slug() {
        return this.$route.params.slug;
      },
    },

    created() {
      document.title = "Tag: #{0} | {1}".format(this.slug, baseTitle);

      this.$store.dispatch('getTags').then(() => {
        this.$store.commit('setTag', this.slug);

        this.$store.dispatch('getAllAlbums').then(() => {
          this.$store.commit('setAlbumsByTag', this.slug);
          this.$store.commit('setAlbumPage', 1);
        });
      });
    },

    filters: {
      pluralize(value) {
        return value === 1 ? '' : 's';
      },
    },
  }
</script>
