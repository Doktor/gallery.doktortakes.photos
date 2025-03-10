<template>
  <section class="pagination">
    <div class="pagination-controls">
      <div class="item" @click="selectPreviousPage">Prev</div>

      <template v-for="n in getPages()">
        <div
          v-if="n !== 'skip'"
          class="item item-condensed"
          :class="{ selected: page === n }"
          :key="n"
          @click="selectPage(n)"
        >
          <span class="item-text">{{ n }}</span>
        </div>
        <PageSkipInput
          v-else
          :key="n"
          @setPage="setPage"
          :page="page"
          :pages="pages"
        />
      </template>

      <div class="item" @click="selectNextPage">Next</div>
    </div>

    <div class="pagination-controls" v-if="itemsPerPageChoices.length > 0">
      <div class="item item-label item-unselectable">
        <span class="item-text">Items per page</span>
      </div>
      <div
        v-for="count in itemsPerPageChoices"
        class="item item-condensed"
        :class="{ selected: count === itemsPerPage }"
        :key="count"
        @click="$emit('setItemsPerPage', count)"
      >
        <span class="item-text">{{ count }}</span>
      </div>
    </div>
  </section>
</template>

<script>
import PageSkipInput from "./PageSkipInput";

const skip = "skip";

export default {
  components: {
    PageSkipInput,
  },

  data() {
    return {
      half: 2,
      margin: 5,
    };
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
        return [...this.range(first, this.margin), skip, last];
      }

      // Right
      if (Math.abs(this.page - last) <= this.half + 1) {
        return [first, skip, ...this.range(last - this.margin, last)];
      }

      // Middle
      return [
        first,
        skip,
        ...this.range(this.page - this.half, this.page + this.half),
        skip,
        last,
      ];
    },

    setPage(page) {
      this.$emit("setPage", page);
    },
    selectPage(page) {
      if (page === this.page || page < 1 || page > this.pages) {
        return;
      }

      this.$emit("setPage", page);
    },
    selectNextPage() {
      this.selectPage(this.page + 1);
    },
    selectPreviousPage() {
      this.selectPage(this.page - 1);
    },
  },

  props: {
    itemsPerPage: {
      type: Number,
      required: true,
    },
    itemsPerPageChoices: {
      type: Array,
      default: () => [],
    },

    page: {
      type: Number,
      required: true,
    },
    pages: {
      type: Number,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.pagination {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;

  @include variables.headings-font();
  font-size: 1.25rem;
  line-height: 1;

  // Prevent selection
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;

  @media (min-width: 901px) {
    justify-content: space-between;
  }
}

.pagination-controls {
  display: grid;
  grid-auto-flow: column;
  gap: 0;

  margin: 0 auto;
  margin-bottom: 0.5rem;

  @media (min-width: 901px) {
    margin: 0;
  }
}

.item {
  display: inline-block;

  background-color: variables.$background-color-2;
  border: 1px solid variables.$background-color-4;
  border-right: 0;
  padding: 8px 12px;

  &:last-child {
    border-right: 1px solid variables.$background-color-4;
  }

  &:not(.item-label) {
    &:hover {
      background-color: variables.$background-color-4;
    }

    &,
    &:hover {
      transition: background-color 0.25s;
    }
  }

  &:not(.item-unselectable) {
    cursor: pointer;

    &.selected,
    &.selected:hover {
      background-color: variables.$text-blue;
      border-color: darken(variables.$text-blue, 10%);

      & + .item {
        border-left: 0;
        box-shadow: -1px 0 0 darken(variables.$text-blue, 10%);
      }
    }
  }
}

.item-text,
.item-icon {
  color: variables.$text-color;
  line-height: 1;
}

.item-condensed .item-text {
  letter-spacing: -1px;
}

.item-page-skip-inactive {
  padding: 8px 10px;
}

.item-page-skip-active {
  width: 80px;
  border-radius: 0;

  &,
  &:hover {
    background-color: variables.$background-color-2;
  }
}
</style>
