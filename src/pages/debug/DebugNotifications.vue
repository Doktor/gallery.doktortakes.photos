<template>
  <FixedWidthContainer :width="800">
    <main>
      <section>
        <h2>Add notification</h2>
        <CustomInput label="Text" v-model="message" />
        <CustomSelect
          label="Status"
          :options="statusOptions"
          v-model="status"
        />

        <button type="button" @click="addNotification">Submit</button>
      </section>

      <section>
        <h2>Add timed notification</h2>

        <CustomInput label="Text" v-model="message" />
        <CustomInput label="Time (ms)" type="number" v-model="timeMs" />
        <CustomSelect
          label="Status"
          :options="statusOptions"
          v-model="status"
        />

        <button type="button" @click="addTimedNotification">Submit</button>
      </section>
    </main>
  </FixedWidthContainer>
</template>

<script>
import CustomInput from "@/components/form/CustomInput";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import CustomSelect from "@/components/form/CustomSelect";

export default {
  components: { CustomSelect, FixedWidthContainer, CustomInput },

  data() {
    return {
      message: "",
      timeMs: 0,
      status: "",
    };
  },

  computed: {
    statusOptions() {
      return ["default", "success", "warning", "error"];
    },
  },

  methods: {
    addNotification() {
      this.$store.commit("addNotification", {
        message: this.message,
        status: this.status,
      });
    },

    addTimedNotification() {
      this.$store.commit("addTimedNotification", {
        message: this.message,
        status: this.status,
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
