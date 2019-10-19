<template>
  <div v-if="!loading">
    <h2>Featured</h2>

    <div v-if="photos.length > 0">
      <section id="featured">
        <div class="container">
          <div class="grid-sizer"></div>
          <div v-for="photo in photos" class="item">
            <router-link
                :to="{name: 'photo', params: {path: photo.path, md5: photo.md5}}">
              <img alt="Photo" :src="photo.thumbnail">
            </router-link>
          </div>
        </div>
      </section>

      <section class="view-more">
        <div class="view-more-wrapper">
          <!-- TODO: query string -->
          <router-link class="view-more-link" :to="{name: 'search'}">
            View more featured photos
          </router-link>
        </div>
      </section>
    </div>

    <p v-else>No featured photos found.</p>
  </div>
</template>

<script>
  import {mapState} from 'vuex';


  export default {
    computed: {
      ...mapState([
        'loading',
        'photos',
      ]),
    },

    created() {
      this.$store.dispatch('getFeaturedPhotos');
    },

    watch: {
      photos() {
        let el = document.querySelector('#featured .container');
        new imagesLoaded(el, function() {
          new Masonry(el, {
            itemSelector: '.item',
          });
        });
      }
    }
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
