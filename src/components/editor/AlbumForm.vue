<template>
  <form class="form--1-column" v-on:submit.prevent="submit">
    <fieldset>
      <div class="form-control">
        <label for="f-name">Name</label>
        <input class="field" name="name" maxlength="256" id="f-name" type="text" v-model="albumEdits.name" required />
      </div>

      <div v-if="isUpdate" class="form-control">
        <label for="f-slug">Slug</label>
        <input class="field" name="slug" id="f-slug" type="text" :value="album.slug" disabled readonly />
      </div>

      <div v-if="isUpdate" class="form-control">
        <label for="f-path">Path</label>
        <input class="field" name="path" id="f-path" type="text" :value="album.path" disabled />
      </div>

      <div class="form-control">
        <label for="f-place">Place</label>
        <input class="field" name="place" maxlength="128" id="f-place" type="text" v-model="albumEdits.place" />
      </div>

      <div class="form-control">
        <label for="f-location">Location</label>
        <input class="field" name="location" maxlength="128" id="f-location" type="text" v-model="albumEdits.location" />
      </div>

      <div class="form-control">
        <label for="f-description">Description</label>
        <textarea
            class="field" name="description" maxlength="1000"
            id="f-description" rows="5" v-model="albumEdits.description"
        ></textarea>
      </div>

      <div class="form-control">
        <label for="f-start">Start</label>
        <input class="field" name="start" id="f-start" type="date" v-model="albumEdits.start" required />
      </div>

      <div class="form-control">
        <label for="f-end">End</label>
        <input class="field" name="end" id="f-end" type="date" v-model="albumEdits.end" />
      </div>

      <div class="form-control">
        <label for="f-level">Access level</label>
        <select
            class="field" name="level" id="f-level"
            v-model="albumEdits.access_level"
        >
          <option v-for="item in accessLevels" :value="item.level">
            {{ item.name }}
          </option>
        </select>
      </div>

      <div class="form-control">
        <label for="f-access-code">Access code</label>
        <input class="field" name="access-code" id="f-access-code" type="text" v-model="albumEdits.access_code" />

        <GenerateAccessCode
            v-on:set-access-code="setAccessCode"
        />
      </div>

      <div class="form-control">
        <label for="f-users">Users</label>
        <input class="field" name="users" id="f-users" type="text" v-model="users" />
      </div>

      <div class="form-control">
        <label for="f-groups">Groups</label>
        <input class="field" name="groups" id="f-groups" type="text" v-model="groups" />
      </div>

      <div class="form-control">
        <label for="f-tags">Tags</label>
        <input class="field" name="tags" id="f-tags" type="text" v-model="tags" />
      </div>

      <div class="form-control">
        <label for="f-parent">Parent</label>
        <input class="field" name="parent" id="f-parent" type="text" v-model="albumEdits.parent" />
      </div>
    </fieldset>

    <button id="album-form-save" type="submit">{{ saveButtonText }}</button>
  </form>
</template>

<script>
import GenerateAccessCode from './GenerateAccessCode.vue';
import {accessLevels} from "@/store";


export default {
  components: {
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
      albumEdits: {...this.album},

      accessLevels,
      users: "",
      groups: "",
      tags: "",
    }
  },

  methods: {
    setAccessCode(value) {
      this.albumEdits.access_code = value;
    },

    submit() {
      for (let key of ["users", "groups", "tags"]) {
        this.albumEdits[key] = this.$data[key].split(',').map(v => v.trim()).filter(v => v.length > 0);
      }

      this.$emit('save', this.albumEdits);
    },
  },

  mounted() {
    this.users = this.album.users.join(", ");
    this.groups = this.album.groups.join(", ");
    this.tags = this.album.tags.join(", ");
  },
}
</script>
