<template>
  <FixedWidthContainer v-if="!loading">
    <h2>Tags</h2>

    <ul v-if="tags" class="tags">
      <li v-for="tag in tags">
        <router-link :to="{name: 'tag', params: {slug: tag.slug}}">
          #{{ tag.slug }}
        </router-link>
      </li>
    </ul>
    <p v-else>No tags found.</p>
  </FixedWidthContainer>
</template>

<script>
  import {mapState} from 'vuex';
  import FixedWidthContainer from "../components/FixedWidthContainer";


  export default {
    components: {
      FixedWidthContainer,
    },

    computed: {
      ...mapState([
        'loading',
        'tags',
      ]),
    },

    created() {
      this.$store.dispatch('getTags');
    },
  }
</script>

<style lang="scss" scoped>
  .tags {
    text-align: left;
    column-width: 250px;
  }
</style>
