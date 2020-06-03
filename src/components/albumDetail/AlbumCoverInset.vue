<template>
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

      <template v-if="userIsStaff">
        <span v-if="album.parent">&middot;</span>

        <router-link
          :to="{name: 'editAlbum', params: {path: album.path}}"
        >
          Edit
        </router-link>

        &middot;

        <a :href="album.admin_url">Admin</a>

        &middot;

        <a
          :href="urlProductionSite"
          title="View album on production site"
          target="_blank"
          rel="noopener noreferrer"
        >Production</a>

        &middot;

        <a
          :href="urlAlphaSite"
          title="View album on alpha site"
          target="_blank"
          rel="noopener noreferrer"
        >Alpha</a>
      </template>
    </div>
  </div>
</template>

<script>
  import {domains} from "../../store";
  import {mapState} from 'vuex';


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


      urlAlphaSite() {
        return new URL(this.album.url, domains.alpha).href;
      },

      urlProductionSite() {
        return new URL(this.album.url, domains.production).href;
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
