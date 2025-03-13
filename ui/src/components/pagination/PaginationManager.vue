<template>
  <section>
    <Pagination
      v-if="showTopControl"
      :itemsPerPage="size"
      :itemsPerPageChoices="sizeOptions"
      @setPage="setPage"
      @setItemsPerPage="setSize"
      :page="page"
      :pages="pages"
    />

    <slot></slot>

    <Pagination
      v-if="showBottomControl"
      :itemsPerPage="size"
      :itemsPerPageChoices="sizeOptions"
      @setPage="setPage"
      @setItemsPerPage="setSize"
      :page="page"
      :pages="pages"
    />
  </section>
</template>

<script>
import Pagination from "./Pagination";

export default {
  components: { Pagination },

  props: {
    showTopControl: {
      type: Boolean,
      default: false,
    },
    showBottomControl: {
      type: Boolean,
      default: true,
    },

    // Client
    allItems: {
      type: Array,
    },

    // Server
    isServerSide: {
      type: Boolean,
      default: false,
    },
    getPage: {
      // (page, size) -> items
      type: Function,
    },

    page: {
      type: Number,
      default: 1,
    },
    size: {
      type: Number,
      default: 12,
    },
    sizeOptions: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      cache: {},
      count: 0,
    };
  },

  computed: {
    pages() {
      return this.isServerSide
        ? Math.ceil(this.count / this.size)
        : Math.ceil(this.allItems.length / this.size);
    },

    indexStart() {
      return this.size * (this.page - 1);
    },
    indexEnd() {
      return this.indexStart + this.size - 1;
    },
  },

  async mounted() {
    if (this.isServerSide) {
      await this.setPage(this.page, true);
    }
  },

  methods: {
    async setPage(page, initial = false) {
      this.$emit("setPage", page);

      if (this.isServerSide) {
        await this.updateServerPaginatedItems(page, this.size);
      }

      let location = { query: { ...this.$route.query, page } };

      if (initial) {
        await this.$router.replace(location);
      } else {
        await this.$router.push(location);
      }

      if (this.isServerSide) {
        return;
      }

      this.$nextTick(() => this.updateClientPaginatedItems());
    },

    async setSize(size) {
      this.$emit("setPage", 1);
      this.$emit("setSize", size);
      this.cache = {};

      if (this.isServerSide) {
        await this.getPageServerSide(1, size);
        return;
      }

      this.$nextTick(() => this.updateClientPaginatedItems());
    },

    updateClientPaginatedItems() {
      let paginatedItems = this.allItems.slice(
        this.indexStart,
        this.indexEnd + 1,
      );

      for (let item of paginatedItems) {
        item.isLoaded = true;
      }

      this.$emit("setPaginatedItems", paginatedItems);
    },

    async updateServerPaginatedItems(page, size) {
      let items, count;

      if (Object.prototype.hasOwnProperty.call(this.cache, page)) {
        items = this.cache[page];
        this.$emit("setPaginatedItems", items);
        return;
      }

      this.$store.commit("setLoading", true);
      this.$emit("setPaginatedItems", Array(size).fill(undefined));

      ({ items, count } = await this.getPage(page, size));

      this.cache[page] = items;
      this.count = count;

      this.$store.commit("setLoading", false);
      this.$emit("setPaginatedItems", items);
    },
  },

  watch: {
    allItems: {
      immediate: true,
      handler(newItems) {
        if (this.isServerSide || newItems.length === 0) {
          return;
        }

        for (let item of newItems) {
          item.isLoaded = false;
        }

        let queryPage = Number.parseInt(this.$route.query?.page);

        if (!Number.isNaN(queryPage)) {
          this.setPage(queryPage);
        } else {
          this.setPage(1, true);
        }

        this.$nextTick(() => this.updateClientPaginatedItems());
      },
    },
  },
};
</script>
