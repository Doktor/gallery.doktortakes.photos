<template>
  <div v-if="pages > 1" class="pagination">
    <span>
      <span
          class="page page-flip"
          @click="selectPreviousPage">
        Prev
      </span>

      <template v-for="n in getPages()">
        <span
            v-if="n !== 'skip'"
            class="page"
            :class="{'page-selected': page === n}"
            @click="selectPage(n)"
        >{{ n }}</span>
        <PageSkipInput v-else :mutation="mutation" :page="page" :pages="pages"/>
      </template>

      <span
          class="page page-flip"
          @click="selectNextPage">
        Next
      </span>
    </span>

    <span class="pagination-items-per-page">
      <span class="page page-select">Items per page</span>
      <span
          v-for="count in itemsPerPageChoices"
          class="page"
          :class="{'page-selected': count === itemsPerPage}"
          @click="setItemsPerPage(count)"
      >
        {{ count }}
      </span>
    </span>
  </div>
</template>

<script>
  import PageSkipInput from './PageSkipInput.vue';


  const skip = 'skip';

  export default {
    components: {
      PageSkipInput,
    },

    data() {
      return {
        half: 2,
        margin: 5,
      }
    },

    methods: {
      range(start, end) {
        return Array.from(new Array(end - start + 1), (x, i) => i + start);
      },

      getPages() {
        let first = 1;
        let last = this.pages;

        if (this.pages <= this.margin + this.half) {
          return this.range(first, last);
        }

        // Left
        if (Math.abs(this.page - first) <= this.half + 1) {
          return [...this.range(first, this.margin), skip, last]
        }

        // Right
        if (Math.abs(this.page - last) <= this.half + 1) {
          return [first, skip, ...this.range(last - this.margin, last)]
        }

        // Middle
        return [
          first, skip,
          ...this.range(this.page - this.half, this.page + this.half),
          skip, last
        ]
      },

      selectPage(page) {
        if (page === this.page || page < 1 || page > this.pages) {
          return;
        }

        this.$store.commit('setPage', {page: page, mutation: this.mutation});
      },
      selectNextPage() {
        this.selectPage(this.page + 1);
      },
      selectPreviousPage() {
        this.selectPage(this.page - 1);
      }
    },

    props: {
      mutation: {
        type: String,
        required: true,
      },
      itemsPerPage: {
        type: Number,
        required: true,
      },
      itemsPerPageChoices: {
        type: Array,
        required: true,
      },
      setItemsPerPage: {
        type: Function,
        required: true,
      },

      page: {
        type: Number,
        required: true,
      },
      pages: {
        type: Number,
        required: true,
      },
    }
  }
</script>

<style scoped>
  .page:not([data-page]) {
    letter-spacing: normal !important;
  }

  .page-flip {
    letter-spacing: -3px !important;
  }

  .page-selected, .page-selected:hover {
    background-color: rgb(0, 120, 255) !important;
  }

  .pagination-items-per-page {
    margin-left: 1rem;
  }
</style>
