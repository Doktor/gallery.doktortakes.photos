<template>
  <div v-if="!loading">
    <section v-if="albums.length">
      <AlbumListCards
          class="albums"
          :albums="albums"
          :indexStart="0"
          :indexEnd="11"
          :route="'album'"
      />

      <div class="view-more">
        <div class="view-more-wrapper">
          <router-link
              class="view-more-link"
              title="View more albums"
              :to="{name: 'albums'}"
          >
            View more albums
          </router-link>
        </div>
      </div>
    </section>
    <div v-else>No albums found.</div>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumListCards from "../components/AlbumListCards.vue";


  export default {
    components: {
      AlbumListCards,
    },

    computed: {
      ...mapState([
        'albums',
        'loading',
      ]),

    },

    created() {
      this.$store.dispatch('getAlbums');
    },
  }
</script>
