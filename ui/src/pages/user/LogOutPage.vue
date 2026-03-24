<template>
  <main>
    <p>Logging out...</p>
  </main>
</template>

<script>
import { useStore } from "@/store";
import { router } from "@/router";

export default {
  async mounted() {
    const store = useStore();
    store.logOut();
    store.addTimedNotification({
      message: "Logged out successfully.",
      hideAfter: 5000,
    });
    router.push({ name: "index" });
  },
};
</script>
