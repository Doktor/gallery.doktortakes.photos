<template>
  <div class="notifications">
    <Notification
      v-for="notification in notifications"
      :key="notification.id"
      :notification="notification"
    />
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useStore } from "@/store";
import Notification from "./Notification";

export default {
  components: {
    Notification,
  },

  computed: {
    ...mapState(useStore, ["notifications"]),
  },
};
</script>

<style lang="scss">
.notifications {
  position: fixed;
  bottom: 0;
  left: 0;

  z-index: 100;

  padding: 1rem;
}
</style>
