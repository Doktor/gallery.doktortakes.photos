<template>
  <FixedWidthContainer :width="800">
    <main>
      <section>
        <h2>Add notification</h2>
        <CustomInput label="Text" v-model="message" />

        <button type="button" @click="addNotification">Submit</button>
      </section>

      <section>
        <h2>Add timed notification</h2>

        <CustomInput label="Text" v-model="message" />
        <CustomInput label="Time (ms)" type="number" v-model="timeMs" />

        <button type="button" @click="addTimedNotification">Submit</button>
      </section>
    </main>
  </FixedWidthContainer>
</template>

<script>
import CustomInput from "@/components/form/CustomInput";
import FixedWidthContainer from "@/components/FixedWidthContainer";

export default {
  components: { FixedWidthContainer, CustomInput },

  data() {
    return {
      message: "",
      timeMs: 0,
    };
  },

  methods: {
    addNotification() {
      this.$store.commit("addNotification", this.message);
    },

    addTimedNotification() {
      this.$store.commit("addTimedNotification", {
        message: this.message,
        hideAfter: this.timeMs,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
main {
  text-align: left;
}

.field {
  max-width: 480px;
}
</style>
