<template>
  <div class="info-metadata">
    <h2>Metadata</h2>

    <dl title="Metadata">
      <div>
        <dt><i title="Sequence number" class="fas fa-fw fa-list-ol"></i></dt>
        <dd>{{ photo.index + 1 }} / {{ count }}</dd>
      </div>

      <div>
        <dt><i title="Date taken" class="fas fa-fw fa-clock"></i></dt>
        <dd>{{ photo.taken }}</dd>
      </div>

      <div>
        <dt><i title="Dimensions" class="fas fa-fw fa-image"></i></dt>
        <dd>{{ photo.width }} &times; {{ photo.height }}</dd>
      </div>

      <div>
        <dt><i title="MD5 checksum" class="fas fa-fw fa-check-circle"></i></dt>
        <dd class="md5">{{ photo.md5.substring(0, 8) }}</dd>
      </div>

      <div>
        <dt><i title="Open in new tab"
               class="fas fa-fw fa-external-link-square-alt"></i></dt>
        <dd><a :href="photo.image" title="Open in new tab">Open in new tab</a></dd>
      </div>

      <div>
        <dt><i title="Download" class="fas fa-fw fa-download"></i></dt>
        <dd><a :href="photo.download" title="Download photo">Download</a></dd>
      </div>

      <div v-if="isStaff">
        <dt><i title="Admin" class="fas fa-fw fa-toolbox"></i></dt>
        <dd><a :href="photo.admin" title="Open in admin site">Admin</a></dd>
      </div>
    </dl>
  </div>
</template>

<script>
  import {mapGetters, mapState} from 'vuex';


  export default {
    computed: {
      ...mapGetters(["isStaff"]),
      ...mapState([
        'user',
      ]),
    },

    props: {
      photo: {
        type: Object,
        required: true,
      },
      count: {
        type: Number,
        required: true,
      },
    },
  }
</script>

<style scoped>
  i {
    margin-right: 6px;
  }

  .md5 {
    font-family: "Consolas", monospace;
    line-height: 1;
    word-break: break-all;
  }
</style>
