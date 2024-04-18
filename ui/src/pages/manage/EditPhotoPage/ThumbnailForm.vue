<template>
  <form class="form--1-column" v-on:submit.prevent="submit">
    <fieldset>
      <CustomInput
        label="Width"
        type="number"
        v-model="request.width"
        required
        :errors="errors.width"
      />
      <CustomInput
        label="Height"
        type="number"
        v-model="request.height"
        required
        :errors="errors.height"
      />

      <CustomInput label="Name" v-model="request.name" />
    </fieldset>

    <CustomButton class="button-primary" @click="submit">
      Create thumbnail
    </CustomButton>
  </form>
</template>

<script>
import CustomInput from "@/components/form/CustomInput";
import CustomSelect from "@/components/form/CustomSelect";
import { ManagePhotoService } from "@/services/manage/ManagePhotoService";
import CustomButton from "@/components/form/CustomButton";

export default {
  components: { CustomButton, CustomSelect, CustomInput },
  props: {
    photo: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      errors: {
        width: [],
        height: [],
      },
      request: {
        width: this.photo.width.toString(),
        height: this.photo.height.toString(),
        name: "",
      },
    };
  },

  methods: {
    parseData() {
      let hasErrors = false;

      let width = parseInt(this.request.width);
      if (Number.isNaN(width)) {
        this.errors.width.push("width should be a number");
        hasErrors = true;
      }

      let height = parseInt(this.request.height);
      if (Number.isNaN(height)) {
        this.errors.height.push("height should be a number");
        hasErrors = true;
      }

      if (hasErrors) {
        return null;
      }

      this.errors.width = [];
      this.errors.height = [];

      return {
        ...this.request,
        width,
        height,
      };
    },
    async submit() {
      let data = this.parseData();

      if (data === null) {
        return;
      }

      let { ok } = await ManagePhotoService.createThumbnail(
        this.photo.md5,
        data,
      );

      if (!ok) {
        this.$store.commit("addNotification", {
          message: "An unknown error occurred.",
          status: "error",
        });
        return;
      }

      this.$store.commit("addNotification", {
        message: "Successfully created thumbnail.",
        status: "success",
      });
      this.$emit("update");
    },
  },
};
</script>
