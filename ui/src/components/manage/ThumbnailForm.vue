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
      <CustomInput
        label="Add watermark"
        type="checkbox"
        v-model="request.addWatermark"
      />
      <CustomSelect
        label="Watermark color"
        v-model="request.watermarkColor"
        :options="watermarkColors"
        :errors="errors.watermarkColor"
      />
    </fieldset>

    <CustomButton class="button-primary" @click="submit">
      Create thumbnail
    </CustomButton>
  </form>
</template>

<script>
import CustomInput from "../form/CustomInput.vue";
import CustomSelect from "../form/CustomSelect.vue";
import { ManagePhotoService } from "@/services/manage/ManagePhotoService";
import CustomButton from "../form/CustomButton.vue";

const watermarkColors = [
  {
    value: "black",
    display: "Black",
  },
  {
    value: "white",
    display: "White",
  },
];

export default {
  name: "ThumbnailForm",
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
        watermarkColor: [],
      },
      request: {
        width: this.photo.width.toString(),
        height: this.photo.height.toString(),
        name: "",
        addWatermark: false,
        watermarkColor: "",
      },
      watermarkColors,
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

      if (this.request.addWatermark && !this.request.watermarkColor) {
        this.errors.watermarkColor.push(
          "watermark color should be set if adding watermark"
        );
        hasErrors = true;
      }

      if (hasErrors) {
        return null;
      }

      this.errors.width = [];
      this.errors.height = [];
      this.errors.watermarkColor = [];

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
        data
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
