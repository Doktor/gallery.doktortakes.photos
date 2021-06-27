<template>
  <FixedWidthContainer v-if="!loading">
    <section>
      <h2>Recently updated albums</h2>

      <Albums v-if="albums.length" :albums="albums" :albumRoute="'album'"/>
      <div v-else>No albums found.</div>
    </section>

    <section>
      <h2>Recent commits</h2>

      <p>
        Last commit:
        <a class="commit-hash" :href="status.commit_link + status.last_commit_hash">{{ status.last_commit_hash.substring(0, 7) }}</a>
        at
        {{ status.last_commit_datetime }} ({{ status.last_commit_naturaltime }})
      </p>

      <ul>
        <li v-for="item in status.last_20_commits">
          <a class="commit-hash" :href="status.commit_link + item.hash">{{ item.hash.substring(0, 7) }}</a>
          &nbsp;{{ item.subject }}
        </li>
      </ul>

      <p>View all commits <a :href="status.commit_list">here</a>.</p>
    </section>
  </FixedWidthContainer>
</template>

<script>
  import {mapState} from 'vuex';
  import Albums from "@/components/albumList/Albums";
  import Photos from '@/components/photoList/Photos.vue';
  import FixedWidthContainer from "@/components/FixedWidthContainer";


  export default {
    components: {
      Albums,
      FixedWidthContainer,
      Photos,
    },

    computed: {
      ...mapState([
        'albums',
        'loading',
      ]),

      status() {
        return this.$store.state.gitStatus;
      }
    },

    created() {
      this.$store.dispatch('getRecent');
    },
  }
</script>

<style scoped>
  section:not(:last-child) {
    margin-bottom: 3rem;
  }
</style>
