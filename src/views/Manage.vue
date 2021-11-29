<template>
  <div v-if="!loading">
    <FixedWidthContainer>
      <h2>Edit</h2>

      <ul>
        <li><router-link :to="{name: 'newAlbum'}">Add new album</router-link></li>
        <li><router-link :to="{name: 'groups'}">View groups</router-link></li>
        <li><router-link :to="{name: 'users'}">View users</router-link></li>
      </ul>
    </FixedWidthContainer>

    <SearchAlbums albumRoute="editAlbum" />
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import SearchAlbums from "@/components/albumList/SearchAlbums";
  import FixedWidthContainer from "@/components/FixedWidthContainer";


  export default {
    components: {
      FixedWidthContainer,
      SearchAlbums,
    },

    computed: {
      ...mapState([
        'albums',
        'loading',
      ]),
    },

    created() {
      this.$store.dispatch('getAllAlbums').then(() => {
        this.$store.commit('setAlbumsToTopLevelAlbums');
      })
    },
  }
</script>
