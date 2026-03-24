<template>
  <div v-if="album.accessLevel > 0">
    <div v-if="!isStaff && album.accessCode" class="overlay-item">
      <i title="Warning" class="fas fa-fw fa-exclamation-triangle"></i>
      <span
        >This is an unlisted link; please don't share the link. If you want to
        share the photos, please download the photos and post them
        directly.</span
      >
    </div>

    <div v-if="isStaff" class="overlay-item">
      <i title="Access level" class="fas fa-fw fa-lock"></i>
      <span>Access level: {{ accessLevelDisplay }}</span>
    </div>

    <div v-if="isStaff && album.accessCode" class="overlay-item">
      <i title="Access code" class="fas fa-fw fa-key"></i>
      <span
        ><!--
      -->Access code:
        <router-link :to="accessCodeRoute">
          {{ album.accessCode }}
        </router-link>
      </span>
    </div>

    <div v-if="isStaff && (hasUsers || hasGroups)" class="overlay-item">
      <i title="Users and groups" class="fas fa-fw fa-users"></i>
      <span>
        <template v-if="hasUsers">Users: {{ album.users.join(", ") }}</template>
        <span v-if="hasUsers && hasGroups" class="divider"></span>
        <template v-if="hasGroups"
          >Groups: {{ album.groups.join(", ") }}</template
        >
      </span>
    </div>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useStore } from "@/store";
import { accessLevelsMap } from "@/constants";

export default {
  props: {
    album: {
      type: Object,
      required: true,
    },
  },

  computed: {
    ...mapState(useStore, ["isStaff"]),
    ...mapState(useStore, ["user"]),

    accessCodeRoute() {
      return {
        name: "album",
        params: {
          pathArray: this.album.pathArray,
        },
        query: {
          code: this.album.accessCode,
        },
      };
    },

    accessLevelDisplay() {
      return accessLevelsMap[this.album.accessLevel];
    },

    hasGroups() {
      return this.album.groups.length > 0;
    },

    hasUsers() {
      return this.album.users.length > 0;
    },
  },
};
</script>

<style lang="scss" scoped>
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
