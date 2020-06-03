<template>
  <div v-if="album.access_level > 0">
    <div v-if="!userIsStaff" class="group-inset-list-item">
      <i title="Warning" class="fas fa-fw fa-exclamation-triangle"></i>
      <span>Please ask before sharing these photos.</span>
    </div>

    <div v-if="userIsStaff" class="group-inset-list-item">
      <i title="Access level" class="fas fa-fw fa-lock"></i>
      <span>Access level: {{ accessLevelDisplay }}</span>
    </div>

    <div v-if="album.access_code" class="group-inset-list-item">
      <i title="Access code" class="fas fa-fw fa-key"></i>
      <span><!--
      -->Access code:
        <router-link :to="accessCodeRoute">
          {{ album.access_code }}
        </router-link>
      </span>
    </div>

    <div
        v-if="album.users.length > 0 || album.groups.length > 0"
        class="group-inset-list-item"
    >
      <i title="Users and groups" class="fas fa-fw fa-users"></i>
      <span><!--
      -->{{ album.users.join(", ") }}<!--
      --><template
          v-if="album.users.length > 0 && album.groups.length > 0">, </template><!--
      -->{{ album.groups.join(", ") }}
      </span>
    </div>
  </div>

</template>

<script>
  import {mapState} from 'vuex';
  import {accessLevelsMap} from "../../store/index.js";


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

      userIsStaff() {
        return this.user.status === 'staff' || this.user.status === 'superuser';
      },
    },
  }
</script>
