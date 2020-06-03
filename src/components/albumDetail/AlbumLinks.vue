<template>
  <div class="group-inset-list-item">
    <i title="Links" class="fas fa-fw fa-link"></i>

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
  </div>
</template>

<script>
  import {domains} from "../../store";
  import {mapState} from 'vuex';


  export default {
    computed: {
      ...mapState([
        'album',
      ]),

      urlAlphaSite() {
        return new URL(this.album.url, domains.alpha).href;
      },

      urlProductionSite() {
        return new URL(this.album.url, domains.production).href;
      },
    },
  }
</script>
