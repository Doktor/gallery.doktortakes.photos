<template>
  <div v-if="!loading">
    <h2>Featured photos</h2>

    <PhotoViewer
        :count="this.photos.length - 1"
        :onClick="onClick"
        :photo="photo"
        :useHistory="false"
    />

    <Filmstrip
        :photos="photos"
        :position="photo.index"
    />

    <section class="view-more">
      <div class="view-more-wrapper">
        <!-- TODO: query string -->
        <router-link class="view-more-link" :to="{name: 'search'}">
          View more featured photos
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
  import {mapState} from 'vuex';

  import Filmstrip from "../components/photo/Filmstrip.vue";
  import PhotoViewer from "../components/PhotoViewer.vue";
  import {router} from "../router/main.js";


  export default {
    components: {
      PhotoViewer,
      Filmstrip,
    },

    computed: {
      ...mapState([
        'loading',
        'photos',
        'photo',
      ]),
    },

    created() {
      this.$store.dispatch('getFeaturedPhotos');
    },

    methods: {
      onClick() {
        router.push({
          name: 'photo',
          params: {
            path: this.photo.path,
            md5: this.photo.md5
          },
        });
      },
    },
  }
</script>

<style lang="scss" scoped>
  $itemSpacing: 0.5rem;

  @mixin fade($t: opacity 0.2s ease-in-out) {
    -webkit-transition: $t;
    -moz-transition: $t;
    -o-transition: $t;
    -ms-transition: $t;
    transition: $t;
  }

  #featured {
    $width: 400px;

    margin: 0 (-$itemSpacing) 1rem (-$itemSpacing);

    .item {
      padding: $itemSpacing;
      width: 100%;

      @media (min-width: $width * 2 + 1) and (max-width: $width * 3) {
        width: (100% / 2);
      }
      @media (min-width: $width * 3 + 1) {
        width: (100% / 3);
      }

      @include fade();
    }

    img {
      width: 100%;
    }
  }
</style>
