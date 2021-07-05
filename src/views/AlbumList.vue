<template>
  <main>
    <div>
      <Albums
        v-if="loading"
        :albums="new Array(12).fill({})"
        :albumRoute="'album'"
        :isSkeleton="true"
      >
        <template #footer />
      </Albums>

      <Albums v-else-if="results.length" :albums="results" :albumRoute="'album'">
        <template #footer>
          <AlbumSearchInput v-model="search" @input="filterAlbums" />
        </template>
      </Albums>

      <div v-else>No albums found.</div>
    </div>
  </main>
</template>

<script>
  import {mapMutations, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import Albums from "@/components/albumList/Albums";
  import AlbumSearchInput from "@/components/albumList/AlbumSearchInput.vue";


  export default {
    components: {
      AlbumSearchInput,
      Albums,
    },

    computed: {
      ...mapFields([
        'search',
      ]),
      ...mapState([
        'results',
        'loading',
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
