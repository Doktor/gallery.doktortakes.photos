<template>
  <Modal @close="$emit('close')">
    <div>
      <h3>Set creator</h3>

      <input
        v-model="creatorName"
        title="Creator name"
        type="text"
        placeholder="Creator name"
      />

      <CustomButton class="button-primary" @click="submit">
        Submit
      </CustomButton>
    </div>
  </Modal>
</template>

<script>
import { useStore } from "@/store";
import CustomButton from "@/components/form/CustomButton";
import Modal from "@/components/Modal.vue";

export default {
  components: {
    Modal,
    CustomButton,
  },

  data() {
    return {
      creatorName: "",
    };
  },

  methods: {
    submit() {
      if (!this.creatorName.trim()) {
        useStore().addNotification({
          message: "The creator name can't be empty.",
          status: "error",
        });
        return;
      }

      this.$emit("submit", this.creatorName.trim());
    },
  },
};
</script>
