<template>
  <form>
    <h2 class="form-title">Search all photos</h2>

    <fieldset>
      <h3 class="fieldset-legend">Sort by</h3>

      <div class="fieldset-contents">
        <div class="form-control">
          <label>Attribute</label>

          <div class="form-control-options">
            <input type="radio" id="taken" name="order" value="taken" checked v-model="order">
            <label for="taken">Taken</label>

            <input type="radio" id="edited" name="order" value="edited" v-model="order">
            <label for="edited">Edited</label>

            <input type="radio" id="uploaded" name="order" value="uploaded" v-model="order">
            <label for="uploaded">Uploaded</label>
          </div>
        </div>

        <div class="form-control">
          <label>Direction</label>

          <div class="form-control-options">
            <input type="radio" id="new" name="direction" value="new" checked v-model="direction">
            <label for="new">Newest first</label>

            <input type="radio" id="old" name="direction" value="old" v-model="direction">
            <label for="old">Oldest first</label>
          </div>
        </div>
      </div>
    </fieldset>

    <fieldset>
      <h3 class="fieldset-legend">Filters</h3>

      <div class="fieldset-contents">
        <div class="form-control">
          <label for="name">Album name</label>
          <input id="name" name="name" title="Album name" type="text" v-model="name">
        </div>

        <div class="form-control">
          <label for="location">Location</label>
          <input id="location" name="location" title="Location" type="text"
                 v-model="location">
        </div>

        <div class="form-control">
          <label>Dimensions</label>

          <div class="form-control-range-input">
            <input id="width" name="width" title="Width" type="text"
                   v-model="width">
            <span class="form-control-input-separator">&times;</span>
            <input id="height" name="height" title="Height" type="text"
                   v-model="height">
          </div>
        </div>

        <div class="form-control">
          <label>Taken</label>

          <div class="form-control-range-input">
            <input id="taken-start" name="taken-start" title="Start" type="date"
                   v-model="takenStart">
            <span class="form-control-input-separator">&ndash;</span>
            <input id="taken-end" name="taken-end" title="End" type="date"
                   v-model="takenEnd">
          </div>
        </div>

        <div class="form-control">
          <label>Uploaded</label>

          <div class="form-control-range-input">
            <input id="uploaded-start" name="uploaded-start" title="Start" type="date"
                   v-model="uploadedStart">
            <span class="form-control-input-separator">&ndash;</span>
            <input id="uploaded-end" name="uploaded-end" title="End" type="date"
                   v-model="uploadedEnd">
          </div>
        </div>

        <div class="form-control">
          <label>Rating</label>

          <div class="form-control-options">
            <template v-for="rating in allRatings">
              <input type="checkbox" :id="'rating-' + rating" name="rating"
                     :value="rating" v-model="ratings">
              <label :for="'rating-' + rating">{{ rating }}</label>
            </template>
          </div>
        </div>
      </div>
    </fieldset>

    <div class="submit-container">
      <button class="submit" type="button" @click="search">Search</button>
    </div>
  </form>
</template>

<script>
  import {mapGetters, mapState} from 'vuex';
  import {getQueryString} from "../store/index.js";


  export default {
    computed: {
      ...mapGetters([
        'photosPerPage',
      ]),

      ...mapState([
        'searchResults',
      ]),

      allRatings() {
        return [0, 1, 2, 3, 4, 5];
      },
    },

    data() {
      return {
        order: "taken",
        direction: "new",

        ratings: [],

        name: "",
        location: "",
        width: "",
        height: "",

        takenStart: null,
        takenEnd: null,
        uploadedStart: null,
        uploadedEnd: null,
      }
    },

    methods: {
      search() {
        this.$store.commit('clearSearchResults');
        this.$store.dispatch('searchPhotos', getQueryString({
          ...this.$data,

          page: this.searchResults.page,
          photosPerPage: this.photosPerPage,
        }));
      }
    },

    watch: {
      'searchResults.page': function() {
        this.search();
      },
    },
  }
</script>

<style lang="scss" scoped>
  form {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: start;
    flex-wrap: wrap;

    width: 100%;

    @media (min-width: 1501px) {
      width: 60%;
      margin: 0 auto;
    }

    text-align: left;
  }

  .form-title {
    margin: 0 1rem;
    width: 100%;

    text-align: center;
  }

  fieldset {
    width: 100%;
    margin: 0;

    @media (min-width: 901px) {
      width: 50%;
    }
  }

  .fieldset-legend {
    text-align: center;
  }

  .fieldset-contents {
    padding: 1rem;
    border: 1px solid rgb(60, 60, 60);
    border-radius: 4px;
    margin: 1rem;

    @media (min-width: 1201px) {
      margin: 1rem 0.5rem;

      fieldset:first-of-type & {
        margin-left: 0;
      }

      fieldset:last-of-type & {
        margin-right: 0;
      }
    }
  }

  label {
    display: inline-block;
    width: auto;
  }

  .form-control-options {
    display: flex;

    input[type="radio"], input[type="checkbox"] {
      display: none;

      & + label {
        display: block;
        flex-basis: 100%;

        &:first-of-type {
          border-radius: 4px 0 0 4px;
        }

        &:last-of-type {
          border-radius: 0 4px 4px 0;
        }
      }
    }
  }

  .form-control {
    margin-bottom: 1.5rem;

    &:last-child {
      margin-bottom: 0;
    }

    label {
      display: block;
      width: 100%;
    }
  }

  // Range inputs

  $separator-width: 5%;

  .form-control-range-input {
    display: flex;

    input[type='text'], input[type='number'], input[type='date'] {
      display: block;
      width: (100% - $separator-width) / 2;
      padding: 8px 16px;
      font-size: 1.2rem;
    }
  }

  .form-control-input-separator {
    width: $separator-width;

    text-align: center;
  }

  // Submit button

  .submit-container {
    display: flex;
    justify-content: center;

    width: 100%;
    margin-top: 1rem;
  }

  .submit {
    text-align: center;

    border: 0;
    border-radius: 4px;
    padding: 8px 16px;

    background-color: rgb(220, 220, 220);
  }
</style>
