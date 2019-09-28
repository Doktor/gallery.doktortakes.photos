<template>
  <section class="album-details">
    <div class="album-cover-container">
      <div class="album" :class="{'album-no-cover': !album.cover}">
        <a v-if="album.cover"
           :href="album.cover.image"
           target="_blank"
           title="Full size">
          <img
              :src="album.cover.thumbnail"
              :title="album.name"
              alt="Album cover image"
          >
        </a>
        <template v-else="album-cover">
          <img
              :src="placeholder"
              :title="album.name"
              alt="Album cover image placeholder"
          >
          <div class="note album-no-cover-note">No cover photo</div>
        </template>
      </div>
    </div>

    <div class="album-form-container">
      <AlbumForm :update="true"/>
    </div>
  </section>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumForm from './AlbumForm.vue';
  import {staticFiles} from "../store/editor";


  export default {
    components: {
      AlbumForm,
    },

    computed: {
      ...mapState([
        'album',
      ]),
    },

    data() {
      return {
        placeholder: staticFiles.coverPlaceholder,
      }
    },
  }
</script>

<style lang="scss">
  .album-details {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;

    margin-top: 1rem;
  }

  .album-form-container, .album-cover-container {
    width: 100%;

    @media (min-width: 1201px) {
      width: 50%;
    }
  }

  .album-cover-container {
    order: 1;

    display: flex;
    justify-content: center;
    margin-bottom: 1rem;

    .album {
      max-width: 600px;
    }

    @media (min-width: 1201px) {
      order: 2;

      display: block;
      margin-bottom: 0;
      padding-left: 0.5rem;

      .album {
        max-width: unset;
        width: 100%;
      }
    }
  }

  .album-form-container {
    order: 2;

    @media (min-width: 1201px) {
      order: 1;
      padding-right: 0.5rem;
    }
  }
</style>
