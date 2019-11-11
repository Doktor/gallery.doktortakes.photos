<template>
  <div class="info-links">
    <h2>Navigation</h2>

    <dl title="Links">
      <div>
        <dt title="Album"><i class="fas fa-fw fa-book"></i></dt>
        <dd>
          <router-link :to="{name: 'album', params: {path: album.pathSplit}}">Return to album</router-link>
        </dd>
      </div>

      <div>
        <dt title="Album list"><i class="fas fa-fw fa-list"></i></dt>
        <dd>
          <router-link :to="{name: 'albums'}">Return to album list</router-link>
        </dd>
      </div>

      <div>
        <dt title="Index"><i class="fas fa-fw fa-home"></i></dt>
        <dd><a href="/">Return home</a></dd>
      </div>
    </dl>
  </div>
</template>

<script>
  import {mapState} from 'vuex';


  export default {
    computed: {
      ...mapState([
        'album',
      ]),
    },
  }
</script>

<style scoped>
  i {
    margin-right: 6px;
  }
</style>
