<template>
  <div v-if="album.access_level > 0">
    <div v-if="!userIsStaff" class="overlay-item">
      <i title="Warning" class="fas fa-fw fa-exclamation-triangle"></i>
      <span>Please ask before sharing these photos.</span>
    </div>

    <div v-if="userIsStaff" class="overlay-item">
      <i title="Access level" class="fas fa-fw fa-lock"></i>
      <span>Access level: {{ accessLevelDisplay }}</span>
    </div>

    <div v-if="album.access_code" class="overlay-item">
      <i title="Access code" class="fas fa-fw fa-key"></i>
      <span><!--
      -->Access code:
        <router-link :to="accessCodeRoute">
          {{ album.access_code }}
        </router-link>
      </span>
    </div>

    <div
      v-if="hasUsers || hasGroups"
      class="overlay-item"
    >
      <i title="Users and groups" class="fas fa-fw fa-users"></i>
      <span>
        <template v-if="hasUsers">Users: {{ album.users.join(", ") }}</template>
        <span
          v-if="hasUsers && hasGroups"
          class="divider"></span>
        <template v-if="hasGroups">Groups: {{ album.groups.join(", ") }}</template>
      </span>
    </div>
  </div>

</template>

<script>
  import {mapState} from 'vuex';
  import {accessLevelsMap} from "@/store/index.js";


  export default {
    computed: {
      ...mapState([
        'album',
        'user',
      ]),

      accessCodeRoute() {
        return {
          name: 'album',
          params: {
            path: this.album.pathSplit,
          },
          query: {
            code: this.album.access_code,
          }
        }
      },

      accessLevelDisplay() {
        return accessLevelsMap[this.album.access_level];
      },

      hasGroups() {
        return this.album.groups.length > 0;
      },

      hasUsers() {
        return this.album.users.length > 0;
      },

      userIsStaff() {
        return this.user.status === 'staff' || this.user.status === 'superuser';
      },
    },
  }
</script>

<style lang="scss" scoped>
  .divider {
    -moz-user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;

    &::before {
      color: rgb(220, 220, 220);
      content: "\00a0\00b7\00a0";  // nbsp, middle dot, nbsp
    }
  }
</style>
