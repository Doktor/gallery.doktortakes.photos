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
        label="Access level"
        :options="accessLevels"
        v-model="changes.access_level"
      />

      <CustomInput label="Access code" v-model="changes.access_code">
        <GenerateAccessCode @setAccessCode="setAccessCode" />
      </CustomInput>

      <template v-if="isUpdate">
        <CustomInput label="Users" v-model="users" />
        <CustomInput label="Groups" v-model="groups" />
        <CustomInput label="Tags" v-model="tags" />

        <CustomInput label="Parent" v-model="changes.parent" />
      </template>
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
      changes: { ...this.album },

      accessLevels,
      users: "",
      groups: "",
      tags: "",
    };
  },

  methods: {
    setAccessCode(value) {
      this.changes.access_code = value;
    },

    submit() {
      let changes = { ...this.changes };

      if (this.isUpdate) {
        for (let key of ["users", "groups", "tags"]) {
          changes[key] = this.$data[key]
            .split(",")
            .map((v) => v.trim())
            .filter((v) => v.length > 0);
        }
      }

      if (!changes.end) {
        changes.end = null;
      }

      this.$emit("save", changes);
    },
  },

  mounted() {
    if (this.isUpdate) {
      this.users = this.album.users.join(", ");
      this.groups = this.album.groups.join(", ");
      this.tags = this.album.tags.join(", ");
    }
  },
};
</script>
