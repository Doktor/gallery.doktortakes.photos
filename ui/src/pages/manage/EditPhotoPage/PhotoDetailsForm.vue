<template>
  <form class="form--1-column" v-on:submit.prevent="submit">
    <fieldset>
      <CustomInput
        label="Creator"
        type="text"
        v-model="request.creator"
      />
      <CustomInput
        label="Description"
        type="textarea"
        v-model="request.description"
      />
    </fieldset>

    <CustomButton class="button-primary" @click="submit">
      Save details
    </CustomButton>
  </form>
</template>

<script>
import { useStore } from "@/store";
import CustomInput from "@/components/form/CustomInput";
import CustomButton from "@/components/form/CustomButton";
import { ManagePhotoService } from "@/services/manage/ManagePhotoService";

export default {
  components: { CustomButton, CustomInput },
  props: {
    photo: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      request: {
        creator: this.photo.creator ?? "",
        description: this.photo.description ?? "",
      },
    };
  },

  methods: {
    async submit() {
      let { ok } = await ManagePhotoService.updatePhoto(
        this.photo.md5,
        {
          creator: this.request.creator || null,
          description: this.request.description,
        },
      );

      if (!ok) {
        useStore().addNotification({
          message: "An unknown error occurred.",
          status: "error",
        });
        return;
      }

      useStore().addNotification({
        message: "Successfully updated photo details.",
        status: "success",
      });
      this.$emit("update");
    },
  },
};
</script>
