<template>
  <form v-on:submit.prevent="submit">
    <fieldset>
      <div class="form-row">
        <label for="f-name">Name</label>
        <div class="field-wrapper">
          <input class="field" name="name" maxlength="256" id="f-name"
                 type="text" v-model="name" required>
        </div>
      </div>

      <div class="form-row">
        <label for="f-slug">Slug</label>
        <div class="field-wrapper">
          <input class="field" name="slug" id="f-slug" type="text"
                 :value="album.slug" disabled readonly>
        </div>
      </div>

      <div class="form-row">
        <label for="f-path">Path</label>
        <div class="field-wrapper">
          <input class="field" name="path" id="f-path" type="text"
                 :value="album.path" disabled>
        </div>
      </div>

      <div class="form-row">
        <label for="f-place">Place</label>
        <div class="field-wrapper">
          <input class="field" name="place" maxlength="128" id="f-place"
                 type="text" v-model="place">
        </div>
      </div>

      <div class="form-row">
        <label for="f-location">Location</label>
        <div class="field-wrapper">
          <input class="field" name="location" maxlength="128" id="f-location"
                 type="text" v-model="location">
        </div>
      </div>

      <div class="form-row">
        <label for="f-description">Description</label>
        <div class="field-wrapper">
          <textarea class="field" name="description" maxlength="1000"
                    id="f-description" rows="5"
                    v-model="description"></textarea>
        </div>
      </div>

      <div class="form-row">
        <label for="f-start">Start</label>
        <div class="field-wrapper">
          <input class="field" name="start" id="f-start" type="date"
                 v-model="start" required>
        </div>
      </div>

      <div class="form-row">
        <label for="f-end">End</label>
        <div class="field-wrapper">
          <input class="field" name="end" id="f-end" v-model="end"
                 type="date">
        </div>
      </div>

      <div class="form-row">
        <label for="f-level">Access level</label>
        <div class="field-wrapper">
          <select class="field" name="level" id="f-level"
                  v-model="access_level">
            <option v-for="item in accessLevels" :value="item.level">
              {{ item.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-row">
        <label for="f-access-code">Access code</label>
        <div class="field-wrapper">
          <input class="field" name="access-code" id="f-access-code"
                 v-model="access_code" type="text">
        </div>

        <GenerateAccessCode
            v-on:set-access-code="setAccessCode"></GenerateAccessCode>
      </div>

      <div class="form-row">
        <label for="f-users">Users</label>
        <div class="field-wrapper">
          <input class="field" name="users" id="f-users"
                 v-model="users" type="text">
        </div>
      </div>

      <div class="form-row">
        <label for="f-groups">Groups</label>
        <div class="field-wrapper">
          <input class="field" name="groups" id="f-groups"
                 v-model="groups" type="text">
        </div>
      </div>

      <div class="form-row">
        <label for="f-tags">Tags</label>
        <div class="field-wrapper">
          <input class="field" name="tags" id="f-tags" type="text"
                 v-model="tags">
        </div>
      </div>

      <div class="form-row">
        <label for="f-parent">Parent</label>
        <div class="field-wrapper">
          <input class="field" name="parent" id="f-parent" type="text"
                 v-model="parent">
        </div>
      </div>
    </fieldset>

    <button id="album-form-save" type="submit">{{ saveButtonText }}</button>
  </form>
</template>

<script>
  import {mapGetters, mapState} from 'vuex';
  import {mapFields} from 'vuex-map-fields';
  import GenerateAccessCode from './GenerateAccessCode.vue';
  import {accessLevels} from '../store/editAlbum';


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
        'album.users',
        'album.groups',
        'album.tags',
        'album.parent',
      ]),
    },

    data() {
      return {
        accessLevels: accessLevels,
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
        this.$store.dispatch('saveAlbum');
      },
    },

    props: {
      saveButtonText: {
        type: String,
        default: "Save",
      },
    },
  }
</script>
