<template>
  <div class="overlay-container" :class="classes">
    <div class="overlay-section">
      <div class="overlay-item">
        <h2 v-if="!isSkeleton" class="title">{{ album.name }}</h2>
        <h2 v-else class="title">Loading...</h2>
      </div>

      <div class="overlay-item" v-if="!loading">
        <span v-html="date"></span>

        <template v-if="photos.length > 0">
          <span> &middot; </span>
          <span>{{ photos.length }} photo{{ photos.length|pluralize }}</span>
        </template>
      </div>
    </div>

    <div class="overlay-section" v-if="!loading">
      <AlbumMetadata class="overlay-item"/>
      <AlbumAccessInfo class="overlay-item"/>
      <AlbumLinks class="overlay-item" v-if="userIsStaff"/>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumAccessInfo from "./AlbumAccessInfo.vue";
  import AlbumLinks from "./AlbumLinks.vue";
  import AlbumMetadata from "./AlbumMetadata.vue";

  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  function twoDigitPad(n) {
    return n <= 9 ? "0" + n : n;
  }

  function formatDate(date) {
    return "{0} {1}-{2}-{3}".format(
      days[date.getDay()],
      date.getFullYear(),
      twoDigitPad(date.getMonth() + 1),
      twoDigitPad(date.getDate())
    )
  }


  export default {
    components: {
      AlbumAccessInfo,
      AlbumLinks,
      AlbumMetadata,
    },

    computed: {
      ...mapState([
        'album',
        'loading',
        'photos',
        'user',
      ]),

      classes() {
        return {
          'is-empty': !this.isSkeleton && this.album.cover === null,
          'is-skeleton': this.isSkeleton,
        }
      },

      date() {
        let start = new Date(this.album.start);
        let end = this.album.end === null ? null : new Date(this.album.end);

        return end === null
          ? formatDate(start)
          : "{0} &ndash; {1}".format(formatDate(start), formatDate(end));
      },

      userIsStaff() {
        return this.user.status === 'staff' || this.user.status === 'superuser';
      },
    },

    filters: {
      pluralize(value) {
        return value === 1 ? '' : 's';
      },
    },

    props: {
      isSkeleton: {
        type: Boolean,
        default: false,
      },
    },
  }
</script>

<style lang="scss" scoped>
  .overlay-container {
    position: relative;
    z-index: 1;
    min-height: 50vh;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    background-color: rgba(0, 0, 0, 0.6);

    &.is-empty, &.is-skeleton {
      min-height: unset;
      background-color: unset;
    }
  }

  .overlay-section {
    padding: 1.8rem;
  }

  .title {
    display: inline-block;
    margin: 0;

    font-size: 3.3rem;
    line-height: 1;
    text-transform: none;
  }

  .overlay-item, ::v-deep .overlay-item {
    @include primary-font();
    font-size: 1.5rem;
    line-height: 1.1;
    text-align: left;
    text-transform: none;
    text-shadow: 1px 1px 2px black;

    margin-bottom: 0.75rem;

    i {
      margin-right: 6px;
    }

    &:last-child {
      margin-bottom: 0;
    }
  }
</style>
