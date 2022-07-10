<template>
  <form class="form--1-column" v-on:submit.prevent="submit">
    <fieldset>
      <CustomInput
        label="Name"
        v-model="changes.name"
        required
        maxlength="256"
      />

      <CustomInput
        v-if="isUpdate"
        label="Slug"
        :value="album.slug"
        disabled
        readonly
      />
      <CustomInput
        v-if="isUpdate"
        label="Path"
        :value="album.path"
        disabled
        readonly
      />

      <CustomInput label="Place" v-model="changes.place" maxlength="128" />
      <CustomInput
        label="Location"
        v-model="changes.location"
        maxlength="128"
      />

      <CustomInput
        label="Description"
        type="textarea"
        v-model="changes.description"
        rows="5"
        maxlength="1000"
      />

      <CustomInput label="Start" type="date" v-model="changes.start" required />
      <CustomInput label="End" type="date" v-model="changes.end" />

      <CustomSelect
        label="Display image size"
        :options="displayImageSizes"
        v-model="changes.display_image_size"
      />

      <CustomSelect
        label="Access level"
        :options="accessLevels"
        v-model="changes.access_level"
      />

      <CustomInput label="Access code" v-model="changes.access_code">
        <template #footer>
          <GenerateAccessCode @setAccessCode="setAccessCode" />
        </template>
      </CustomInput>

      <ListInput label="Users" v-model="changes.users" />
      <ListInput label="Groups" v-model="changes.groups" />
      <ListInput label="Tags" v-model="changes.tags" />

      <CustomInput label="Parent" v-model="changes.parent" />
    </fieldset>

    <button id="album-form-save" type="submit">{{ saveButtonText }}</button>
  </form>
</template>

<script>
import GenerateAccessCode from "./GenerateAccessCode.vue";
import CustomInput from "@/components/form/CustomInput";
import CustomSelect from "@/components/form/CustomSelect";
import ListInput from "@/components/form/ListInput";
import { accessLevels } from "@/constants";

const displayImageSizes = [
  {
    value: "2400",
    display: "2400 x 1600",
  },
  {
    value: "3000",
    display: "3000 x 2000",
  },
  {
    value: "3600",
    display: "3600 x 2400",
  },
  {
    value: "3840",
    display: "3840 x 2560",
  },
  {
    value: "4800",
    display: "4800 x 3200",
  },
  {
    value: "6000",
    display: "6000 x 4000",
  },
];

export default {
  components: {
    ListInput,
    CustomSelect,
    CustomInput,
    GenerateAccessCode,
  },

  props: {
    album: {
      type: Object,
      required: true,
    },

    isUpdate: {
      type: Boolean,
      default: false,
    },
    saveButtonText: {
      type: String,
      default: "Save",
    },
  },

  data() {
    return {
      changes: { ...this.album },

      accessLevels,
      displayImageSizes,
    };
  },

  methods: {
    setAccessCode(value) {
      this.changes.access_code = value;
    },

    submit() {
      let changes = { ...this.changes };

      if (!changes.end) {
        changes.end = null;
      }

      this.$emit("save", changes);
    },
  },
};
</script>
