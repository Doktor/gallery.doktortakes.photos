<template>
  <div v-if="!loading">
    <h2>#{{ tag.slug }}</h2>

    <div class="album-search-container">
      <input
          type="text"
          placeholder="Search by name..."
          v-model="search"
          @keyup="filterAlbums"
      >
    </div>

    <div class="count">
      {{ results.length }} album{{ results.length|pluralize}}
    </div>

    <Albums v-if="results.length" :albums="results" :albumRoute="'album'"/>
    <div v-else>No albums found.</div>
  </div>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "../components/Albums.vue";
  import AlbumListDetailedCards from "../components/AlbumListDetailedCards.vue";
  import AlbumListSimple from "../components/AlbumListSimple.vue";


  export default {
    components: {
      Albums,
      AlbumListDetailedCards,
      AlbumListSimple,
    },

    computed: {
      ...mapFields([
        'search',
      ]),
      ...mapState([
        'albums',
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
      this.$store.dispatch('getTag', this.slug);
      this.$store.dispatch('getAllAlbums').then(() => {
        this.$store.commit('setAlbumsByTag', this.slug);
        this.$store.commit('setAlbumPage', 1);
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
