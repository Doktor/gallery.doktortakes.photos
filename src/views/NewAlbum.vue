<template>
  <div>
    <router-link :to="{name: 'editorIndex'}">Back to editor</router-link>
    <h2>Create new album</h2>
    <AlbumForm
        class="form--small"
        :save-button-text="'Create album'"
        :update="false"
    />
  </div>
</template>

<script>
  import AlbumForm from '../components/AlbumForm.vue';
  import {mapState} from 'vuex';


  export default {
    components: {
      AlbumForm,
    },

    computed: {
      ...mapState([
        'album',
      ]),
    },

    created() {
      this.$store.commit('clearAlbum');
    }
  }
</script>
