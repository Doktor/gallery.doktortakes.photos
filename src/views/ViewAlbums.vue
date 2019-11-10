<template>
  <div v-if="!loading">
    <div>
      <h2>Special pages</h2>
      <ul>
        <li v-if="user.status !== 'anonymous'">
          <router-link
              title="User albums"
              :to="{name: 'user', params: {slug: user.name}}"
          >
            View your albums
          </router-link>
        </li>
        <li><router-link title="Tags" :to="{name: 'tags'}">View all tags</router-link></li>
        <li><router-link title="Search" :to="{name: 'search'}">Search all photos</router-link></li>
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
        'results',
        'loading',
        'user',
      ]),
    },

    created() {
      this.$store.dispatch('getAllAlbums').then(() => {
        this.$store.commit('setAlbumsToAllAlbums');
        this.$store.commit('setAlbumPage', 1);
      })
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
