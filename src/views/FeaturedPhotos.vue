<template>
  <div v-if="!loading">
    <div class="featured-photos">
      <div class="featured-photo" v-for="photo in photos">
        <div class="featured-photo-sizer">
          <router-link title="" :to="photo.url">
            <LazyImage class="featured-photo-image" :src="photo.thumbnail" alt="" :width="600" :height="600" />
          </router-link>
        </div>
      </div>
    </div>

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
  import Filmstrip from "@/components/photoDetail/Filmstrip";
  import LazyImage from "@/components/LazyImage";
  import PhotoViewer from "@/components/photoDetail/PhotoViewer";


  export default {
    components: {
      Filmstrip,
      LazyImage,
      PhotoViewer,
    },

    computed: {
      ...mapState([
        'loading',
        'photos',
        'photo',
      ]),
    },

    async created() {
      await this.$store.dispatch('getFeaturedPhotos');
    },
  }
</script>

<style lang="scss" scoped>
$spacing: 0.3rem;
$width: 600px;

.featured-photos {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;

  margin: 0 (-$spacing);
}

.featured-photo {
  padding: $spacing;

  @media (max-width: $width * 2) {
    width: 100%;
  }
  @for $i from 2 through 5 {
    @media (min-width: $width * ($i) + 1) and(max-width: $width * ($i + 1)) {
      width: 100% / ($i + 1); // 50%, 33%, 25%, 20%
    }
  }
  @media (min-width: $width * 6 + 1) {
    width: (100% / 6); // 16.67%
  }
}

.featured-photo-sizer {
  position: relative;

  width: 100%;
  height: 0;
  padding-bottom: 100%;
}

.featured-photo-image {
  width: 100%;
  height: 100%;
  position: absolute;

  ::v-deep img {
    display: block;
    position: absolute;

    width: 100%;
    height: 100%;

    object-fit: cover;
  }
}
</style>
