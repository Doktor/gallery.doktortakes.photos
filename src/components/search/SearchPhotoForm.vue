<template>
  <form class="form--2-columns">
    <div class="form-column form-column-1">
      <fieldset>
        <legend>Sort by</legend>

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
      </fieldset>

      <fieldset>
        <legend>Items per page</legend>

        <div class="form-control">
          <div class="form-control-options">
            <template v-for="count in countChoices">
              <input
                  type="radio"
                  :id="'f-per-page-' + count"
                  name="perPage"
                  :value="count"
                  v-model="itemsPerPage"
              >
              <label :for="'f-per-page-' + count">{{ count }}</label>
            </template>
          </div>
        </div>
      </fieldset>
    </div>

    <div class="form-column form-column-2">
      <fieldset>
        <legend>Filters</legend>

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
            <span class="form-control-range-input-separator">&times;</span>
            <input id="height" name="height" title="Height" type="text"
                   v-model="height">
          </div>
        </div>

        <div class="form-control">
          <label>Taken</label>

          <div class="form-control-range-input">
            <input id="taken-start" name="taken-start" title="Start" type="date"
                   v-model="takenStart">
            <span class="form-control-range-input-separator">&ndash;</span>
            <input id="taken-end" name="taken-end" title="End" type="date"
                   v-model="takenEnd">
          </div>
        </div>

        <div class="form-control">
          <label>Uploaded</label>

          <div class="form-control-range-input">
            <input id="uploaded-start" name="uploaded-start" title="Start" type="date"
                   v-model="uploadedStart">
            <span class="form-control-range-input-separator">&ndash;</span>
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
      </fieldset>
    </div>

    <div class="form-buttons">
      <button
          class="form-button form-button-primary"
          type="button"
          @click="search"
      >
        Search
      </button>
    </div>
  </form>
</template>

<script>
  import {mapState} from 'vuex';
  import {getQueryString} from "../../store";


  export default {
    computed: {
      ...mapState([
        'searchResults',
      ]),

      allRatings() {
        return [0, 1, 2, 3, 4, 5];
      },

      countChoices() {
        return [10, 30, 60, 120];
      },
    },

    data() {
      return {
        order: "taken",
        direction: "new",
        itemsPerPage: 10,

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
      search(resetPage = true) {
        if (resetPage) {
          this.$store.commit('setSearchResultsPage', 1);
          this.$store.commit('setSearchResultsItemsPerPage', this.itemsPerPage);
        }

        this.$store.commit('clearSearchResults');
        this.$store.dispatch('searchPhotos', getQueryString({
          ...this.$data,

          page: this.searchResults.page,
          itemsPerPage: this.itemsPerPage,
        }));
      }
    },

    watch: {
      'searchResults.page': function() {
        this.search(false);
      },
    },
  }
</script>

<style lang="scss" scoped>
  .form-buttons {
    justify-content: center;
  }

  form {
    @media (min-width: 1501px) {
      width: 60%;
      margin: 0 auto;
    }
  }
</style>
