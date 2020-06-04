<template>
  <main>
    <FixedWidthContainer>
      <h2>Albums</h2>

      <div class="count">
        {{ results.length }} album{{ results.length|pluralize}}
      </div>

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
      <Albums
        v-if="loading"
        :albums="new Array(12).fill({})"
        :albumRoute="'album'"
        :isSkeleton="true"
      />
      <Albums v-else-if="results.length" :albums="results" :albumRoute="'album'"/>
      <div v-else>No albums found.</div>
    </div>

    <FixedWidthContainer>
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
    </FixedWidthContainer>
  </main>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "../components/albumList/Albums.vue";
  import FixedWidthContainer from "../components/FixedWidthContainer.vue";


  export default {
    components: {
      Albums,
      FixedWidthContainer,
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

    async created() {
      await this.$store.dispatch('getAllAlbums');
      this.$store.commit('setAlbumsToTopLevelAlbums');
      this.$store.commit('setAlbumPage', 1);
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
