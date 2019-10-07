<template>
  <div v-if="!loading">
    <!-- TODO: Better placement -->
    <router-link :to="{name: 'albums'}">Back to albums</router-link>

    <section class="group">
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
            <template v-if="album.location">
              <span>{{ album.location }}</span> &middot;
            </template>
            <span v-html="date"></span> &middot;
            <span>{{ photos.length }} photo{{ photos.length|pluralize }}</span>
          </div>

          <div v-if="album.parent || userIsStaff" class="group-inset-text">
            <router-link
                v-if="album.parent"
                :to="{name: 'album', params: {path: album.parent}}"
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

      <div class="group-info">
        <template v-if="album.access_level > 0">
          <div v-if="!userIsStaff" class="group-info-item">
            <i title="Warning" class="fas fa-fw fa-exclamation-triangle"></i>
            Please ask before sharing these photos.
          </div>

          <div v-if="userIsStaff" class="group-info-item">
            <i title="Access level" class="fas fa-fw fa-lock"></i>
            <span>Access level: {{ accessLevelDisplay }}</span>
          </div>

          <div v-if="album.access_code" class="group-info-item">
            <i title="Access code" class="fas fa-fw fa-key"></i>
            <span><!--
            -->Access code:
              <router-link :to="accessCodeRoute">
                {{ album.access_code }}
              </router-link>
            </span>
          </div>

          <div v-if="album.users || album.groups" class="group-info-item">
            <i title="Users and groups" class="fas fa-fw fa-users"></i>
            <span><!--
            -->{{ album.users }}<!--
            --><template v-if="album.users && album.groups">, </template><!--
            -->{{ album.groups }}
            </span>
          </div>
        </template>

        <div v-if="album.tags" class="group-info-item">
          <i title="Tags" class="fas fa-fw fa-tags"></i>
          <span>
            <template v-for="(slug, index) in tags">
              <router-link class="tag" :to="{name: 'tag', params: {slug: slug}}">#{{ slug }}</router-link>
              <span v-if="index !== tags.length - 1" v-html="nbsp"></span>
            </template>
          </span>
        </div>

        <div v-if="album.description"
             class="group-info-item group-description">
          <i title="Description" class="fas fa-fw fa-book"></i>
          <span v-html="album.description"></span>
        </div>
      </div>
    </section>

    <Albums v-if="album.children" :albums="album.children"/>

    <Photos :photos="photos" :allowSelect="false"/>
  </div>
</template>

<script>
  import Albums from "../components/Albums.vue";
  import Photos from '../components/Photos.vue';
  import {mapState} from 'vuex';
  import {accessLevelsMap, staticFiles} from "../store/editor";


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
      Albums,
      Photos,
    },

    computed: {
      ...mapState([
        'album',
        'loading',
        'photos',
        'user',
      ]),

      accessCodeRoute() {
        return {
          name: 'album',
          params: {
            path: this.album.path,
          },
          query: {
            access_code: this.album.access_code,
          }
        }
      },

      accessLevelDisplay() {
        return accessLevelsMap[this.album.access_level];
      },

      date() {
        let start = new Date(this.album.start);
        let end = this.album.end === null ? null : new Date(this.album.end);

        return end === null
          ? formatDate(start)
          : "{0} &ndash; {1}".format(formatDate(start), formatDate(end));
      },

      nbsp() {
        return "&nbsp;";
      },

      path() {
        return this.$route.params.path;
      },

      placeholder() {
        return staticFiles.coverPlaceholder;
      },

      tags() {
        return this.album.tags.split(', ');
      },

      userIsStaff() {
        return this.user.status === 'staff' || this.user.status === 'superuser';
      },
    },

    created() {
      this.$store.dispatch('getAlbum', {
        path: this.path,
        setDocumentTitle: 'updateDocumentTitle',
      });

      document.body.classList.remove('small');
    },

    filters: {
      pluralize(value) {
        return value === 1 ? '' : 's';
      },
    },
  }
</script>
