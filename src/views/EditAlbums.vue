<template>
  <div id="app">
    <template v-if="!loading">
      <h2><a href="/albums/new/">Add new album</a></h2>

      <h2>Edit existing album</h2>

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

      <Albums v-if="results.length" :albums="results"/>
      <div v-else>No albums found.</div>
    </template>
  </div>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "../components/Albums.vue";


  export default {
    components: {
      Albums,
    },

    computed: {
      ...mapFields([
        'search',
      ]),
      ...mapState([
        'albums',
        'results',
        'loading',
      ]),
    },

    created() {
      this.$store.dispatch('getAlbums');
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
