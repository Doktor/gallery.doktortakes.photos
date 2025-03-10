<template>
  <footer class="nav-footer">
    <div v-if="tagline" class="nav-tagline">
      "<span v-html="tagline"></span>"
    </div>

    <div>
      website & photos
      <router-link :to="{ name: 'copyright' }">&copy; Doktor</router-link>
    </div>
  </footer>
</template>

<script>
import { TaglineService } from "@/services/TaglineService";

export default {
  name: "NavFooter",

  data() {
    return {
      tagline: "",
    };
  },

  async created() {
    this.tagline = await TaglineService.getTagline();
  },
};
</script>

<style lang="scss">
.nav-tagline {
  @include variables.headings-font();
  color: variables.$text-color;
  //font-size: 1.6rem;
  font-weight: 400;

  margin: 1rem 0;
  width: 100%;
}
</style>
