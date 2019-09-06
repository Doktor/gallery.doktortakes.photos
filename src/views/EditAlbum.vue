<template>
  <div id="app">
    <template v-if="!loading">
      <header>
        <h2 id="album-name">{{ album.name }}</h2>

        <ul class="edit-links-center">
          <li>
            <a
                :href="album.url"
                title="View album"
                target="_blank"
            >View</a>
          </li>
          <li>
            <a
                :href="album.admin_url"
                title="View album on admin site"
            >Admin</a>
          </li>
        </ul>
      </header>

      <h2>Album details</h2>
      <AlbumDetails/>

      <PhotoUploader/>
      <PhotoManager/>

      <DeleteAlbum/>
    </template>
  </div>
</template>

<script>
  import AlbumDetails from '../components/AlbumDetails.vue';
  import DeleteAlbum from '../components/DeleteAlbum.vue';
  import PhotoManager from '../components/PhotoManager.vue';
  import PhotoUploader from '../components/PhotoUploader.vue';
  import {mapState} from 'vuex';


  export default {
    components: {
      AlbumDetails,
      DeleteAlbum,
      PhotoManager,
      PhotoUploader,
    },

    computed: {
      ...mapState([
        'album',
        'loading',
      ]),
    },

    created() {
      this.$store.dispatch('getData');
    },

    mounted() {
      this.$store.commit('changePage', 1);
    },
  }
</script>

<style lang="scss" scoped>
  body {
    max-width: 1100px;
    margin-bottom: 3rem;
  }

  section {
    margin: 2rem 0;
  }

  h2 {
    margin: 0.5rem 0;
  }

  #album-form-save {
    align-self: flex-end;
  }
</style>
