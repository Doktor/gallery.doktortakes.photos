<template>
  <div class="pagination">
    <span>
      <span
          class="item"
          @click="selectPreviousPage">
        Prev
      </span>

      <template v-for="n in getPages()">
        <span
            v-if="n !== 'skip'"
            class="item item-condensed"
            :class="{'selected': page === n}"
            :key="n"
            @click="selectPage(n)"
        >{{ n }}</span>
        <PageSkipInput
            v-else
            :key="n"
            :setPage="setPage"
            :page="page"
            :pages="pages"
        />
      </template>

      <span
          class="item"
          @click="selectNextPage">
        Next
      </span>
    </span>

    <span v-if="itemsPerPageChoices.length > 0">
      <span class="item item-label item-unselectable">Items per page</span>
      <span
          v-for="count in itemsPerPageChoices"
          class="item item-condensed"
          :class="{'selected': count === itemsPerPage}"
          :key="count"
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

        this.setPage(page);
      },
      selectNextPage() {
        this.selectPage(this.page + 1);
      },
      selectPreviousPage() {
        this.selectPage(this.page - 1);
      }
    },

    props: {
      itemsPerPage: {
        type: Number,
        required: true,
      },
      setItemsPerPage: {
        type: Function,
      },
      itemsPerPageChoices: {
        type: Array,
        default: () => [],
      },

      page: {
        type: Number,
        required: true,
      },
      setPage: {
        type: Function,
        required: true,
      },

      pages: {
        type: Number,
        required: true,
      },
    }
  }
</script>

<style lang="scss" scoped>
$itemBackgroundColor: rgb(40, 40, 40);

.pagination {
  display: flex;
  justify-content: space-between;

  @include secondary-headings-font();
  text-align: left;
  font-size: 1.25rem;
  line-height: 1;
  letter-spacing: unset;

  margin: 0;

  // Prevent selection
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.item {
  display: inline-block;

  color: gainsboro;
  background-color: $itemBackgroundColor;
  border: 1px solid rgb(80, 80, 80);
  border-right: 0;
  padding: 8px 12px;

  line-height: 1;

  &:last-child {
    border-right: 1px solid rgb(80, 80, 80);
  }

  &:not(.item-label) {
    &:hover {
      background-color: rgb(80, 80, 80);
    }

    &, &:hover {
      transition: background-color 0.25s;
    }
  }

  &:not(.item-unselectable) {
    cursor: pointer;

    &.selected, &.selected:hover {
      background-color: $blue;
    }
  }
}

.item-condensed {
  letter-spacing: -1px;
}

.item-page-skip-inactive {
  padding: 8px 10px;
}

.item-page-skip-active {
  width: 80px;
  border-radius: 0;

  &, &:hover {
    background-color: $itemBackgroundColor;
  }
}
</style>
