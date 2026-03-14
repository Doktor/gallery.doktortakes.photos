<template>
  <FixedWidthContainer v-if="!loading">
    <h2>Tags</h2>

    <ul v-if="tags" class="tags">
      <li v-for="tag in tags">
        <router-link :to="{ name: 'tag', params: { slug: tag.slug } }">
          #{{ tag.slug }}
        </router-link>
      </li>
    </ul>
    <p v-else>No tags found.</p>
  </FixedWidthContainer>
</template>

<script>
import { mapState } from "vuex";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import { TagService } from "@/services/TagService";

export default {
  components: {
    FixedWidthContainer,
  },

  computed: {
    ...mapState(["loading"]),
  },

  data() {
    return {
      tags: [],
    };
  },

  async created() {
    this.$store.commit("setBreadcrumbs", [
      {
        label: "Tags",
        to: { name: "tags" },
      },
    ]);

    this.$store.commit("setLoading", true);
    this.tags = await TagService.getTags();
    this.$store.commit("setLoading", false);
  },
};
</script>

<style lang="scss" scoped>
.tags {
  text-align: left;
  column-count: 3;
  column-width: 250px;
}
</style>
