<template>
  <figure
      class="group-cover"
      :class="{'group-cover-no-image': album.cover === null}"
  >
    <img
        v-if="album.cover !== null"
        alt="Cover photo"
        :src="album.cover.thumbnail"
        :title="album.name"
    >
    <img
        v-else
        alt="Cover photo placeholder"
        :src="placeholder"
        :title="album.name"
    >

    <div class="group-inset">
      <div class="group-inset-row">
        <h2 class="group-inset-text group-title">{{ album.name }}</h2>
      </div>

      <div class="group-inset-text">
        <span v-if="location">{{ location }} &middot; </span>
        <span v-html="date"></span> &middot;
        <span>{{ photos.length }} photo{{ photos.length|pluralize }}</span>
      </div>

      <div v-if="album.parent || userIsStaff" class="group-inset-text">
        <router-link
            v-if="album.parent"
            :to="{name: 'album', params: {path: album.parent.split('/')}}"
        >
          View parent album
        </router-link>

        <template v-if="album.parent && userIsStaff"> &middot;</template>

        <router-link
            v-if="userIsStaff"
            :to="{name: 'editAlbum', params: {path: album.path}}"
        >
          Edit
        </router-link>

        &middot;

        <!-- TODO: Admin site link -->
        <a href="/admin/">Admin</a>
      </div>
    </div>
  </figure>
</template>


<script>
  import {mapState} from 'vuex';
  import {staticFiles} from "../store/index.js";


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
    computed: {
      ...mapState([
        'album',
        'photos',
        'user',
      ]),

      date() {
        let start = new Date(this.album.start);
        let end = this.album.end === null ? null : new Date(this.album.end);

        return end === null
          ? formatDate(start)
          : "{0} &ndash; {1}".format(formatDate(start), formatDate(end));
      },

      location() {
        let place = this.album.place;
        let location = this.album.location;

        if (place && location) {
          return "{0}, {1}".format(place, location);
        }

        return place || location || "";
      },

      placeholder() {
        return staticFiles.coverPlaceholder;
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
  }
</script>
