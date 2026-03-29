<template>
  <div>
    <i title="Links" class="fas fa-fw fa-link"></i>

    <router-link
      v-if="showManage"
      class="album-link"
      title="Manage album"
      :to="{ name: 'editAlbum', params: { pathArray: album.pathArray } }"
      >Manage</router-link
    >
    <router-link
      v-else
      class="album-link"
      title="View album"
      :to="{
        name: album.type === 'external' ? 'externalAlbum' : 'album',
        params: { pathArray: album.pathArray },
      }"
      >View</router-link
    >

    <span class="divider"></span>

    <a
      :href="album.adminUrl"
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
  </div>
</template>

<script>
import { domains } from "@/constants";

export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
    showManage: {
      type: Boolean,
      default: true,
    },
  },

  computed: {
    urlProductionSite() {
      return new URL(this.album.url, domains.production).href;
    },
  },
};
</script>

<style scoped lang="scss">
@use "@/styles/variables";

.divider {
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;

  &::before {
    color: variables.$text-color;
    content: "\00a0\00b7\00a0"; // nbsp, middle dot, nbsp
  }
}
</style>
