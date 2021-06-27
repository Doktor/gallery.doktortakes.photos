<template>
  <div id="messages">
    <Notification
        v-for="message in notifications"
        :key="message"
        :message="message"
    />
  </div>
</template>

<script>
  import {mapState} from 'vuex';
  import Notification from "@/components/Notification";


  export default {
    components: {
      Notification,
    },

    computed: {
      ...mapState([
        'notifications',
      ]),
    },
  }
</script>
