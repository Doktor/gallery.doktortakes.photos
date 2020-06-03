<template>
  <div class="group-inset-container">
    <div class="group-inset-header">
      <div class="group-inset-row">
        <h2 class="group-inset-text group-title">{{ album.name }}</h2>
      </div>

      <div class="group-inset-text">
        <span v-html="date"></span> &middot;
        <span>{{ photos.length }} photo{{ photos.length|pluralize }}</span>
      </div>
    </div>

    <div class="group-inset-body">
      <div v-if="location" class="group-inset-list-item">
        <i title="Location" class="fas fa-fw fa-map-marker-alt"></i>
        <span>{{ location }}</span>
      </div>

      <AlbumAccessInfo/>

      <div v-if="album.tags.length > 0" class="group-inset-list-item">
        <i title="Tags" class="fas fa-fw fa-tags"></i>
        <span>
          <template v-for="(slug, index) in album.tags">
            <router-link
              class="tag"
              :to="{name: 'tag', params: {slug: slug}}"
              ><!--
                -->#{{ slug }}<!--
              --></router-link>
            <span v-if="index !== album.tags.length - 1" v-html="nbsp"></span>
          </template>
        </span>
      </div>

      <div v-if="album.description"
          class="group-inset-list-item group-description">
        <i title="Description" class="fas fa-fw fa-book"></i>
        <span v-html="album.description"></span>
      </div>

      <div v-if="album.parent" class="group-inset-list-item">
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
