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

    <SearchAlbums :albums="albums" :loading="loading" albumRoute="editAlbum" />
  </div>
</template>

<script>
  import SearchAlbums from "@/components/albumList/SearchAlbums";
  import FixedWidthContainer from "@/components/FixedWidthContainer";
  import {AlbumService} from "@/services/AlbumService";


  export default {
    components: {
      FixedWidthContainer,
      SearchAlbums,
    },

    data() {
      return {
        albums: [],
        loading: true,
      }
    },

    async created() {
      this.loading = true;
      this.albums = await AlbumService.getAllAlbums();
      this.loading = false;
    },
  }
</script>
