<template>
  <div>
    <i title="Links" class="fas fa-fw fa-link"></i>

    <router-link
      class="album-link"
      :to="{ name: 'editAlbum', params: { path: album.path } }"
      >Edit
    </router-link>

    <span class="divider"></span>

    <a
      :href="album.admin_url"
      class="album-link"
      title="View album on admin site"
      >Admin</a
    >

    <span class="divider"></span>

    <a
      :href="urlProductionSite"
      class="album-link"
      title="View album on production site (new tab)"
      target="_blank"
      rel="noopener noreferrer"
      >Production</a
    >

    <span class="divider"></span>

    <a
      :href="urlAlphaSite"
      class="album-link"
      title="View album on alpha site (new tab)"
      target="_blank"
      rel="noopener noreferrer"
      >Alpha</a
    >
  </div>
</template>

<script>
import { domains } from "@/store";

export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
  },

  computed: {
    urlAlphaSite() {
      return new URL(this.album.url, domains.alpha).href;
    },

    urlProductionSite() {
      return new URL(this.album.url, domains.production).href;
    },
  },
};
</script>

<style scoped lang="scss">
.divider {
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;

  &::before {
    color: $text-color;
    content: "\00a0\00b7\00a0"; // nbsp, middle dot, nbsp
  }
}
</style>
