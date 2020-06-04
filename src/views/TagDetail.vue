<template>
  <div>
    <FixedWidthContainer v-if="!loading && tag !== null">
      <h2>#{{ tag.slug }}</h2>

      <div class="album-search-container">
        <input
            type="text"
            placeholder="Search by name..."
            v-model="search"
            @keyup="filterAlbums"
        >
      </div>
    </FixedWidthContainer>

    <div>
      <div class="count">
        {{ results.length }} album{{ results.length|pluralize}}
      </div>

      <Albums v-if="results.length" :albums="results" :albumRoute="'album'"/>
      <div v-else>No albums found.</div>
    </div>
  </div>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "../components/albumList/Albums.vue";
  import AlbumListSimple from "../components/albumList/AlbumListSimple.vue";
  import FixedWidthContainer from "../components/FixedWidthContainer.vue";
  import {baseTitle} from "../router/main.js";


  export default {
    components: {
      Albums,
      AlbumListSimple,
      FixedWidthContainer,
    },

    computed: {
      ...mapFields([
        'search',
      ]),
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

      view() {
        return this.$route.query.view;
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

    methods: {
      ...mapMutations([
        'filterAlbums',
      ]),
    },
  }
</script>
