<template>
  <div id="app">
    <router-link :to="{name: 'editorIndex'}">Back to editor</router-link>

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

      <template>
        <h2>Related albums</h2>

        <router-link
            v-if="album.parent !== null"
            :to="{name: 'editAlbum', params: {path: album.parent.split('/')}}">
          Edit parent album
        </router-link>

        <AlbumChildren :route="'editAlbum'"/>
      </template>

      <PhotoUploader :path="album.path"/>
      <PhotoManager/>

      <DeleteAlbum/>
    </template>
  </div>
</template>

<script>
  import AlbumCard from '../components/AlbumCard.vue';
  import AlbumChildren from "../components/AlbumChildren.vue";
  import AlbumDetails from '../components/AlbumDetails.vue';
  import DeleteAlbum from '../components/DeleteAlbum.vue';
  import PhotoManager from '../components/PhotoManager.vue';
  import PhotoUploader from '../components/PhotoUploader.vue';
  import {mapState} from 'vuex';


  export default {
    components: {
      AlbumCard,
      AlbumChildren,
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
      this.loadAlbum();
    },

    methods: {
      loadAlbum() {
        this.$store.dispatch('getAlbum', this.routePath).then(() => {
          this.$store.commit('setPhotoPage', 1);
          this.$store.commit('updateDocumentTitleForEditAlbum');
        });
      },
    },

    watch: {
      routePath() {
        this.loadAlbum();
      },
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
    margin-top: 2rem;
    margin-bottom: 2rem;
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
