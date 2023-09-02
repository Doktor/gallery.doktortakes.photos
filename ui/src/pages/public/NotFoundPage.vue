<template>
  <FixedWidthContainer class="content">
    <h2>Page not found</h2>
    <p>
      <code class="path">{{ path }}</code> was not found.
    </p>
    <p>
      <router-link :to="{ name: 'albums' }"
        >Return to photos archive</router-link
      >
    </p>
  </FixedWidthContainer>
</template>

<script>
import FixedWidthContainer from "@/components/FixedWidthContainer";

export default {
  components: { FixedWidthContainer },

  computed: {
    path() {
      return this.$route.params.pathMatch;
    },
  },
};
</script>

<style lang="scss" scoped>
.content {
  text-align: center;
}
</style>
