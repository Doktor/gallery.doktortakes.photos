<template>
  <section>
    <Pagination
      :itemsPerPage="size"
      :itemsPerPageChoices="sizeOptions"
      @setPage="setPage"
      @setItemsPerPage="setSize"
      :page="page"
      :pages="pages"
    />

    <slot></slot>

    <Pagination
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
    isServerSide: {
      type: Boolean,
      default: false,
    },

    clientSideItems: {
      type: Array,
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
        : Math.ceil(this.clientSideItems.length / this.size);
    },
  },

  async mounted() {
    if (this.isServerSide) {
      await this.setPage(this.page);
    }
  },

  methods: {
    async getPageServerSide(page, size) {
      let items, count;

      if (Object.prototype.hasOwnProperty.call(this.cache, page)) {
        items = this.cache[page];
      } else {
        ({ items, count } = await this.getPage(page, size));

        this.cache[page] = items;
        this.count = count;
      }

      this.$emit("setItems", items);
    },

    async setPage(page) {
      this.$emit("setPage", page);

      if (this.isServerSide) {
        await this.getPageServerSide(page, this.size);
      }

      await this.$router.push({ query: { page } });
    },

    async setSize(size) {
      this.$emit("setPage", 1);
      this.$emit("setSize", size);
      this.cache = {};

      if (this.isServerSide) {
        await this.getPageServerSide(1, size);
        return;
      }

      this.clientSideItems.forEach((item, index) => {
        item.page = Math.floor(index / this.size) + 1;
      });
    },
  },

  watch: {
    clientSideItems: {
      immediate: true,
      handler(newItems) {
        if (this.isServerSide || newItems.length === 0) {
          return;
        }

        for (let [index, item] of newItems.entries()) {
          item.index = index;
          item.page = Math.floor(index / this.size) + 1;
          item.loaded = false;
        }

        this.$emit("setItems", newItems);

        let queryPage = Number.parseInt(this.$route.query?.page);

        if (!Number.isNaN(queryPage)) {
          this.setPage(queryPage);
        } else {
          this.setPage(1);
        }
      },
    },
  },
};
</script>
