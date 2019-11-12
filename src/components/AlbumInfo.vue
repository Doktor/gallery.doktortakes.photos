<template>
  <div class="group-info">
    <AlbumInfoAccess/>

    <div v-if="album.tags.length > 0" class="group-info-item">
      <i title="Tags" class="fas fa-fw fa-tags"></i>
      <span>
        <template v-for="(slug, index) in album.tags">
          <router-link class="tag"
                       :to="{name: 'tag', params: {slug: slug}}">#{{ slug }}</router-link>
          <span v-if="index !== album.tags.length - 1" v-html="nbsp"></span>
        </template>
      </span>
    </div>

    <div v-if="album.description"
         class="group-info-item group-description">
      <i title="Description" class="fas fa-fw fa-book"></i>
      <span v-html="album.description"></span>
    </div>
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import AlbumInfoAccess from "./AlbumInfoAccess.vue";


  export default {
    components: {
      AlbumInfoAccess,
    },

    computed: {
      ...mapState([
        'album',
      ]),

      nbsp() {
        return "&nbsp;";
      },
    },
  }
</script>
