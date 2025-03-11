<template>
  <form class="form--1-column" @submit.prevent="submit">
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
        v-model="album.slug"
        disabled
        readonly
      />
      <CustomInput
        v-if="isUpdate"
        label="Path"
        v-model="album.path"
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
        label="License"
        :options="licenseOptions"
        v-model="changes.licenseId"
      />

      <CustomSelect
        label="Access level"
        :options="accessLevels"
        v-model="changes.accessLevel"
      />

      <CustomInput label="Access code" v-model="changes.accessCode">
        <template #footer>
          <GenerateAccessCode @setAccessCode="setAccessCode" />
        </template>
      </CustomInput>

      <ListInput label="Users" v-model="changes.users" />
      <ListInput label="Groups" v-model="changes.groups" />
      <ListInput label="Tags" v-model="changes.tags" />

      <CustomInput label="Parent" v-model="changes.parent" />
    </fieldset>

    <CustomButton class="button-primary" type="submit">
      {{ saveButtonText }}
    </CustomButton>
  </form>
</template>

<script>
import GenerateAccessCode from "./GenerateAccessCode";
import CustomInput from "../form/CustomInput";
import CustomSelect from "../form/CustomSelect";
import ListInput from "../form/ListInput";
import { accessLevels } from "@/constants";
import CustomButton from "../form/CustomButton";

export default {
  components: {
    CustomButton,
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

    licenseOptions: {
      type: Array,
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
      changes: {},

      accessLevels,
    };
  },

  methods: {
    setAccessCode(value) {
      this.changes.accessCode = value;
    },

    submit() {
      if (!this.changes.end) {
        this.changes.end = null;
      }

      this.$emit("save", this.changes);
    },
  },

  watch: {
    album: {
      immediate: true,
      handler(newAlbum, oldAlbum) {
        this.changes = structuredClone(newAlbum);
      },
    },
  },
};
</script>
