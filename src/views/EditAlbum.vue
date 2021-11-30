<template>
  <FixedWidthContainer>
    <router-link :to="{name: 'manage'}">Back to editor</router-link>

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
          <li>
            <a
              :href="urlProductionSite"
              title="View album on production site"
              target="_blank"
              rel="noopener noreferrer"
            >Production</a>
          </li>
          <li>
            <a
              :href="urlAlphaSite"
              title="View album on alpha site"
              target="_blank"
              rel="noopener noreferrer"
            >Alpha</a>
          </li>
        </ul>
      </header>

      <h2>Album details</h2>
      <AlbumDetails/>

      <template v-if="album.parent || album.children.length > 0">
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
  </FixedWidthContainer>
</template>

<script>
  import AlbumCard from '@/components/albumList/AlbumCard.vue';
  import AlbumChildren from "@/components/albumList/AlbumChildren";
  import AlbumDetails from '@/components/editor/AlbumDetails.vue';
  import FixedWidthContainer from "@/components/FixedWidthContainer";
  import DeleteAlbum from '@/components/editor/DeleteAlbum.vue';
  import PhotoManager from '@/components/editor/PhotoManager.vue';
  import PhotoUploader from '@/components/editor/PhotoUploader.vue';
  import {mapState} from 'vuex';
  import {domains} from '@/store';


  export default {
    components: {
      AlbumCard,
      AlbumChildren,
      AlbumDetails,
      DeleteAlbum,
      FixedWidthContainer,
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
      },

      urlAlphaSite() {
        return new URL(this.album.url, domains.alpha).href;
      },

      urlProductionSite() {
        return new URL(this.album.url, domains.production).href;
      },
    },

    async created() {
      await this.loadAlbum();
    },

    methods: {
      async loadAlbum() {
        await this.$store.dispatch('getAlbum', {rawPath: this.routePath, code: ""});
        this.$store.commit('updateDocumentTitleForEditAlbum');
      },
    },

    watch: {
      async routePath() {
        await this.loadAlbum();
      },
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
