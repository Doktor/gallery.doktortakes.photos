<template>
  <div id="app">
    <router-link :to="{name: 'index'}">Back to editor</router-link>

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

      <PhotoUploader :path="album.path.join('/')"/>
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

      routePath() {
        return this.$route.params.path;
      }
    },

    created() {
      this.$store.dispatch('getAlbum', {
        routePath: this.routePath,
        setDocumentTitle: 'updateDocumentTitleForEditor',
      });
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

  .count {
    line-height: 1;
    margin: 1rem 0;
  }

  .manage-photos {
    margin: 1rem 0;
  }

  .photo-actions {
    display: flex;
    justify-content: space-between;
  }

  .delete-album {
    display: flex;
    max-width: 600px;
  }
</style>
