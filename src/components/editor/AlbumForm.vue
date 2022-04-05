<template>
  <form class="form--1-column" v-on:submit.prevent="submit">
    <fieldset>
      <CustomInput
        label="Name"
        :value="albumEdits.name"
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

      <CustomInput label="Place" v-model="albumEdits.place" maxlength="128" />
      <CustomInput
        label="Location"
        v-model="albumEdits.location"
        maxlength="128"
      />

      <CustomInput
        label="Description"
        type="textarea"
        v-model="albumEdits.description"
        rows="5"
        maxlength="1000"
      />

      <CustomInput
        label="Start"
        type="date"
        v-model="albumEdits.start"
        required
      />
      <CustomInput label="End" type="date" v-model="albumEdits.end" />

      <CustomSelect
        label="Access level"
        :options="accessLevels"
        v-model="albumEdits.access_level"
      />

      <CustomInput label="Access code" v-model="albumEdits.access_code">
        <GenerateAccessCode @setAccessCode="setAccessCode" />
      </CustomInput>

      <CustomInput label="Users" v-model="users" />
      <CustomInput label="Groups" v-model="groups" />
      <CustomInput label="Tags" v-model="tags" />

      <CustomInput label="Parent" v-model="albumEdits.parent" />
    </fieldset>

    <button id="album-form-save" type="submit">{{ saveButtonText }}</button>
  </form>
</template>

<script>
import GenerateAccessCode from "./GenerateAccessCode.vue";
import { accessLevels } from "@/store";
import CustomInput from "@/components/form/CustomInput";
import CustomSelect from "@/components/form/CustomSelect";

export default {
  components: {
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
      albumEdits: { ...this.album },

      accessLevels,
      users: "",
      groups: "",
      tags: "",
    };
  },

  methods: {
    setAccessCode(value) {
      this.albumEdits.access_code = value;
    },

    submit() {
      for (let key of ["users", "groups", "tags"]) {
        this.albumEdits[key] = this.$data[key]
          .split(",")
          .map((v) => v.trim())
          .filter((v) => v.length > 0);
      }

      this.$emit("save", this.albumEdits);
    },
  },

  mounted() {
    this.users = this.album.users.join(", ");
    this.groups = this.album.groups.join(", ");
    this.tags = this.album.tags.join(", ");
  },
};
</script>
