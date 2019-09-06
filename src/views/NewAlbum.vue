<template>
  <div id="app">
    <AlbumForm
        class="form-small"
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
  }
</script>
