<template>
  <form class="form--1-column" v-on:submit.prevent="submit">
    <fieldset>
      <div class="form-control">
        <label for="f-name">Name</label>
        <input class="field" name="name" maxlength="256" id="f-name" type="text" v-model="name" required>
      </div>

      <div v-if="update" class="form-control">
        <label for="f-slug">Slug</label>
        <input class="field" name="slug" id="f-slug" type="text" :value="album.slug" disabled readonly>
      </div>

      <div v-if="update" class="form-control">
        <label for="f-path">Path</label>
        <input class="field" name="path" id="f-path" type="text" :value="album.path" disabled>
      </div>

      <div class="form-control">
        <label for="f-place">Place</label>
        <input class="field" name="place" maxlength="128" id="f-place" type="text" v-model="place">
      </div>

      <div class="form-control">
        <label for="f-location">Location</label>
        <input class="field" name="location" maxlength="128" id="f-location" type="text" v-model="location">
      </div>

      <div class="form-control">
        <label for="f-description">Description</label>
        <textarea class="field" name="description" maxlength="1000"
                  id="f-description" rows="5" v-model="description"></textarea>
      </div>

      <div class="form-control">
        <label for="f-start">Start</label>
        <input class="field" name="start" id="f-start" type="date" v-model="start" required>
      </div>

      <div class="form-control">
        <label for="f-end">End</label>
        <input class="field" name="end" id="f-end" type="date" v-model="end">
      </div>

      <div class="form-control">
        <label for="f-level">Access level</label>
        <select class="field" name="level" id="f-level"
                v-model="access_level">
          <option v-for="item in accessLevels" :value="item.level">
            {{ item.name }}
          </option>
        </select>
      </div>

      <div class="form-control">
        <label for="f-access-code">Access code</label>
        <input class="field" name="access-code" id="f-access-code" type="text" v-model="access_code">

        <GenerateAccessCode
            v-on:set-access-code="setAccessCode"></GenerateAccessCode>
      </div>

      <div class="form-control">
        <label for="f-users">Users</label>
        <input class="field" name="users" id="f-users" type="text" v-model="users">
      </div>

      <div class="form-control">
        <label for="f-groups">Groups</label>
        <input class="field" name="groups" id="f-groups" type="text" v-model="groups">
      </div>

      <div class="form-control">
        <label for="f-tags">Tags</label>
        <input class="field" name="tags" id="f-tags" type="text" v-model="tags">
      </div>

      <div class="form-control">
        <label for="f-parent">Parent</label>
        <input class="field" name="parent" id="f-parent" type="text" v-model="parent">
      </div>
    </fieldset>

    <button id="album-form-save" type="submit">{{ saveButtonText }}</button>
  </form>
</template>

<script>
  import {mapGetters, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import GenerateAccessCode from './GenerateAccessCode.vue';
  import {accessLevels} from "../../store";


  export default {
    components: {
      GenerateAccessCode,
    },

    computed: {
      ...mapGetters({
        accessCode: 'getAccessCode',
      }),
      ...mapState([
        'album',
      ]),
      ...mapFields([
        'album.name',
        'album.place',
        'album.location',
        'album.description',
        'album.start',
        'album.end',
        'album.access_level',
        'album.access_code',
        'album.parent',
      ]),
    },

    data() {
      return {
        accessLevels: accessLevels,
        users: "",
        groups: "",
        tags: "",
      }
    },

    methods: {
      setAccessCode(value) {
        this.$store.commit('setAlbumField', {
          key: 'access_code',
          value: value
        });
      },

      submit() {
        for (let key of ["users", "groups", "tags"]) {
          this.$store.commit('setAlbumField', {
            key: key,
            value: this.$data[key].split(',').map(v => v.trim()).filter(v => v.length > 0),
          });
        }

        this.$store.dispatch(this.update ? 'saveAlbum' : 'createAlbum');
      },
    },

    mounted() {
      this.users = this.album.users.join(", ");
      this.groups = this.album.groups.join(", ");
      this.tags = this.album.tags.join(", ");
    },

    props: {
      saveButtonText: {
        type: String,
        default: "Save",
      },
      update: {
        type: Boolean,
        required: true,
      },
    },
  }
</script>
