<template>
  <div class="overlay-container">
    <div class="overlay-section overlay-header">
      <div class="overlay-item">
        <h2 class="title">{{ album.name }}</h2>
      </div>

      <div class="overlay-item">
        <span v-html="date"></span> &middot;
        <span>{{ photos.length }} photo{{ photos.length|pluralize }}</span>
      </div>
    </div>

    <div class="overlay-section overlay-body">
      <div v-if="location" class="overlay-item">
        <i title="Location" class="fas fa-fw fa-map-marker-alt"></i>
        <span>{{ location }}</span>
      </div>

      <AlbumAccessInfo class="overlay-item"/>

      <div v-if="album.tags.length > 0" class="overlay-item">
        <i title="Tags" class="fas fa-fw fa-tags"></i>
        <span>
          <template v-for="(slug, index) in album.tags">
            <router-link
              class="tag"
              :key="slug"
              :to="{name: 'tag', params: {slug: slug}}"
              ><!--
                -->#{{ slug }}<!--
              --></router-link>
            <span
              v-if="index !== album.tags.length - 1"
              v-html="nbsp"
              :key="'space-' + index.toString()"></span>
          </template>
        </span>
      </div>

      <div v-if="album.description" class="overlay-item">
        <i title="Description" class="fas fa-fw fa-book"></i>
        <span v-html="album.description"></span>
      </div>

      <div v-if="album.parent" class="overlay-item">
        <i title="Parent album" class="fas fa-fw fa-chevron-circle-up"></i>
        <router-link
          :to="{name: 'album', params: {path: album.parent.split('/')}}"
        ><!--
          -->View parent album<!--
        --></router-link>
      </div>

      <AlbumLinks v-if="userIsStaff"/>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumAccessInfo from "./AlbumAccessInfo.vue";
  import AlbumLinks from "./AlbumLinks.vue";

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
    },

    computed: {
      ...mapState([
        'album',
        'photos',
        'user',
      ]),

      location() {
        let place = this.album.place;
        let location = this.album.location;

        if (place && location) {
          return "{0}, {1}".format(place, location);
        }

        return place || location || "";
      },

      nbsp() {
        return "&nbsp;";
      },

      userIsStaff() {
        return this.user.status === 'staff' || this.user.status === 'superuser';
      },

      date() {
        let start = new Date(this.album.start);
        let end = this.album.end === null ? null : new Date(this.album.end);

        return end === null
          ? formatDate(start)
          : "{0} &ndash; {1}".format(formatDate(start), formatDate(end));
      },
    },

    filters: {
      pluralize(value) {
        return value === 1 ? '' : 's';
      },
    },
  }
</script>

<style lang="scss" scoped>
  .overlay-container {
    position: absolute;
    left: 0;
    top: 0;

    background-color: rgba(0, 0, 0, 0.6);

    width: 100%;
    height: 100%;
  }

  .overlay-section {
    position: absolute;
    left: 0;

    padding: 1.8rem;
  }

  .overlay-header {
    top: 0;
  }

  .overlay-body {
    bottom: 0;
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
