<template>
  <div v-if="!loading">
    <div>
      <h2>Special pages</h2>
      <ul>
        <!-- TODO: Add user albums link -->
        <li><a title="User albums" href="">View your albums</a></li>
        <li><router-link title="Tags" :to="{name: 'tags'}">View all tags</router-link></li>
        <li><a title="Search" href="search/">Search all photos</a></li>
      </ul>
    </div>

    <div>
      <h2>Albums</h2>

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
      document.body.classList.add('small');
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
