<template>
  <form class="form--2-columns">
    <div class="form-column form-column-1">
      <fieldset>
        <legend>Sort by</legend>

        <div class="form-control">
          <label>Attribute</label>

          <div class="form-control-options">
            <input
              type="radio"
              id="taken"
              name="order"
              value="taken"
              checked
              v-model="order"
            />
            <label for="taken">Taken</label>

            <input
              type="radio"
              id="edited"
              name="order"
              value="edited"
              v-model="order"
            />
            <label for="edited">Edited</label>

            <input
              type="radio"
              id="uploaded"
              name="order"
              value="uploaded"
              v-model="order"
            />
            <label for="uploaded">Uploaded</label>
          </div>
        </div>

        <div class="form-control">
          <label>Direction</label>

          <div class="form-control-options">
            <input
              type="radio"
              id="new"
              name="direction"
              value="new"
              checked
              v-model="direction"
            />
            <label for="new">Newest first</label>

            <input
              type="radio"
              id="old"
              name="direction"
              value="old"
              v-model="direction"
            />
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
              />
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
          <input
            id="name"
            name="name"
            title="Album name"
            type="text"
            v-model="name"
          />
        </div>

        <div class="form-control">
          <label for="location">Location</label>
          <input
            id="location"
            name="location"
            title="Location"
            type="text"
            v-model="location"
          />
        </div>

        <div class="form-control">
          <label>Dimensions</label>

          <div class="form-control-range-input">
            <input
              id="width"
              name="width"
              title="Width"
              type="text"
              v-model="width"
            />
            <span class="form-control-range-input-separator">&times;</span>
            <input
              id="height"
              name="height"
              title="Height"
              type="text"
              v-model="height"
            />
          </div>
        </div>

        <div class="form-control">
          <label>Taken</label>

          <div class="form-control-range-input">
            <input
              id="taken-start"
              name="taken-start"
              title="Start"
              type="date"
              v-model="takenStart"
            />
            <span class="form-control-range-input-separator">&ndash;</span>
            <input
              id="taken-end"
              name="taken-end"
              title="End"
              type="date"
              v-model="takenEnd"
            />
          </div>
        </div>

        <div class="form-control">
          <label>Uploaded</label>

          <div class="form-control-range-input">
            <input
              id="uploaded-start"
              name="uploaded-start"
              title="Start"
              type="date"
              v-model="uploadedStart"
            />
            <span class="form-control-range-input-separator">&ndash;</span>
            <input
              id="uploaded-end"
              name="uploaded-end"
              title="End"
              type="date"
              v-model="uploadedEnd"
            />
          </div>
        </div>
      </fieldset>
    </div>

    <div class="form-buttons">
      <CustomButton class="button-primary" @click="search">
        Search
      </CustomButton>
    </div>
  </form>
</template>

<script>
import { getQueryString } from "@/utils";
import { endpoints } from "@/constants";
import CustomButton from "../form/CustomButton";
import { getAsync } from "@/request";

export default {
  components: { CustomButton },
  props: {
    results: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      order: "taken",
      direction: "new",
      itemsPerPage: 24,

      name: "",
      location: "",
      width: "",
      height: "",

      takenStart: null,
      takenEnd: null,
      uploadedStart: null,
      uploadedEnd: null,
    };
  },

  computed: {
    countChoices() {
      return [24, 48, 96];
    },
  },

  methods: {
    async search(resetPage = true) {
      let results = { ...this.results };

      if (resetPage) {
        results.page = 1;
        results.itemsPerPage = this.itemsPerPage;
      }

      results.photos = Array(this.itemsPerPage).fill({ isLoaded: false });
      this.$emit("setResults", results);

      let query = getQueryString({
        ...this.$data,
        page: this.results.page,
        itemsPerPage: this.itemsPerPage,
      });

      let { content } = await getAsync(endpoints.searchPhotos + query);

      results.photos = content.photos.map((photo) => {
        return { ...photo, isLoaded: true };
      });
      results.count = content.count;

      this.$emit("setResults", results);
    },
  },

  watch: {
    "results.page": function () {
      this.search(false);
    },
  },
};
</script>

<style lang="scss" scoped>
.form-buttons {
  justify-content: center;
}

form {
  @media (width >= variables.$full-layout-breakpoint + 1) {
    width: 60%;
    margin: 0 auto;
  }
}
</style>
