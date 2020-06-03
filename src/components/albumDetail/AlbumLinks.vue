<template>
  <div class="group-inset-list-item">
    <i title="Links" class="fas fa-fw fa-link"></i>

    <router-link
      class="album-link"
      :to="{name: 'editAlbum', params: {path: album.path}}"
    >Edit</router-link>

    <a
      :href="album.admin_url"
      class="album-link"
      title="View album on admin site"
    >Admin</a>

    <a
      :href="urlProductionSite"
      class="album-link"
      title="View album on production site (new tab)"
      target="_blank"
      rel="noopener noreferrer"
    >Production</a>

    <a
      :href="urlAlphaSite"
      class="album-link"
      title="View album on alpha site (new tab)"
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

<style scoped lang="scss">
  .album-link {

    &:not(:last-child)::after {
      color: rgb(220, 220, 220);
      content: "\00a0\00b7\00a0";  // nbsp, middle dot, nbsp
    }
  }
</style>
