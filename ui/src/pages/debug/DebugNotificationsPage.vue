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

        <CustomButton class="button-primary" @click="addNotification">
          Submit
        </CustomButton>
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

        <CustomButton class="button-primary" @click="addTimedNotification">
          Submit
        </CustomButton>
      </section>
    </main>
  </FixedWidthContainer>
</template>

<script>
import { useStore } from "@/store";
import CustomInput from "@/components/form/CustomInput";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import CustomSelect from "@/components/form/CustomSelect";
import CustomButton from "@/components/form/CustomButton";

export default {
  components: { CustomButton, CustomSelect, FixedWidthContainer, CustomInput },

  created() {
    useStore().setBreadcrumbs([
      { label: "Debug" },
      {
        label: "Notifications",
        to: {
          name: "debugNotifications",
        },
      },
    ]);
  },

  data() {
    return {
      message: "",
      timeMs: 0,
      status: "",
    };
  },

  computed: {
    statusOptions() {
      return ["default", "success", "warning", "error"].map((status) => {
        return { value: status, display: status };
      });
    },
  },

  methods: {
    addNotification() {
      useStore().addNotification({
        message: this.message,
        status: this.status,
      });
    },

    addTimedNotification() {
      useStore().addTimedNotification({
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
