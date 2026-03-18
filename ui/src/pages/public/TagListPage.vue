<template>
  <FixedWidthContainer v-if="!loading">
    <h2>Tags</h2>

    <section>
      <template
        v-if="tagGroups"
        v-for="[namespace, tags] in Object.entries(tagGroups)"
      >
        <h3 v-if="namespace">{{ namespace }}</h3>

        <ul class="tags">
          <li v-for="tag in tags">
            <router-link :to="{ name: 'tag', params: { slug: tag.slug } }">
              #{{ tag.slug }}
            </router-link>
          </li>
        </ul>
      </template>

      <p v-else>No tags found.</p>
    </section>
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
      tagGroups: {},
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

    const tags = await TagService.getTags();
    this.tagGroups = Object.groupBy(tags, (tag) => tag.namespace);

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
