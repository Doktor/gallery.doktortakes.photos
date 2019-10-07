<template>
  <section v-if="!loading">
    <h2>Tags</h2>

    <ul v-if="tags" class="tags">
      <li v-for="tag in tags">
        <router-link :to="{name: 'tag', params: {path: tag.slug}}">
          #{{ tag.slug }}
        </router-link>
      </li>
    </ul>
    <p v-else>No tags found.</p>
  </section>
</template>

<script>
  import {mapState} from 'vuex';


  export default {
    computed: {
      ...mapState([
        'loading',
        'tags',
      ]),
    },

    created() {
      this.$store.dispatch('getTags');
      document.body.classList.add('small');
    },
  }
</script>

<style lang="scss" scoped>
  .tags {
    text-align: left;
  }
</style>
