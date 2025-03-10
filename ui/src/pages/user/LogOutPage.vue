<template>
  <main>
    <p>Logging out...</p>
  </main>
</template>

<script>
import { router } from "@/router";

export default {
  async mounted() {
    await this.$store.commit("logOut");
    await this.$store.commit("addTimedNotification", {
      message: "Logged out successfully.",
      hideAfter: 5000,
    });
    router.push({ name: "index" });
  },
};
</script>
