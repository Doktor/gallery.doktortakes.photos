<template>
  <section class="filters" v-if="hasCategories">
    <h2>Filters</h2>

    <div class="categories">
      <template
        class="category"
        v-for="[category, values] in Object.entries(categories)"
        :key="category"
      >
        <span class="category-label">{{ category }}</span>

        <div class="category-items">
          <CustomButton
            class="category-item"
            v-for="item in values"
            :key="item.value"
            :isActive="isItemActive(category, item.value)"
            @click="toggleCategoryItem(category, item.value)"
          >
            {{ item.label }} ({{ item.count }})
          </CustomButton>
        </div>
      </template>
    </div>

    <CustomButton v-if="isAnyFilterActive" @click="clearFilters">
      Clear all filters
    </CustomButton>
  </section>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import CustomButton from "@/components/form/CustomButton.vue";

// Helpers

const categoryGetters = {
  creator: (photo) => photo.creator ?? null,
  camera: (photo) => photo.exif?.camera ?? null,
};

function createDefaultFilters() {
  return {
    creator: new Set(),
    camera: new Set(),
  };
}

// Component

const props = defineProps({
  photos: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["update:filteredPhotos"]);

const filters = ref(createDefaultFilters());

const isAnyFilterActive = computed(() =>
  Object.values(filters.value).some((category) => category.size > 0),
);

const categories = computed(() => {
  const result = {};

  for (const [category, getValue] of Object.entries(categoryGetters)) {
    const counts = new Map();

    for (const photo of filteredPhotos.value) {
      const value = getValue(photo);
      counts.set(value, (counts.get(value) || 0) + 1);
    }

    result[category] = counts
      .entries()
      .map(([value, count]) => ({
        value,
        label: value ?? "Unknown",
        count,
      }))
      .toArray();
  }

  return result;
});

const hasCategories = computed(() => Object.keys(categories.value).length > 0);

const filteredPhotos = computed(() => {
  if (!isAnyFilterActive.value) {
    return props.photos;
  }

  return props.photos.filter((photo) => {
    for (let [category, getValue] of Object.entries(categoryGetters)) {
      if (
        filters.value[category].size > 0 &&
        !filters.value[category].has(getValue(photo))
      ) {
        return false;
      }
    }

    return true;
  });
});

function toggleCategoryItem(category, value) {
  const values = new Set(filters.value[category]);

  if (values.has(value)) {
    values.delete(value);
  } else {
    values.add(value);
  }

  filters.value = { ...filters.value, [category]: values };
}

function clearFilters() {
  filters.value = createDefaultFilters();
}

function isItemActive(category, value) {
  return filters.value[category]?.has(value) ?? false;
}

watch(
  () => props.photos,
  () => clearFilters(),
);

watch(filteredPhotos, (value) => emit("update:filteredPhotos", value), {
  immediate: true,
});
</script>

<style lang="scss" scoped>
@use "@/styles/variables";

.filters {
  margin: 24px 0 32px 0;

  text-align: left;
}

.categories {
  display: grid;
  grid-template-columns: min-content 1fr;
  justify-items: left;
  align-items: center;
  gap: 16px;

  margin-bottom: 16px;
}

.category-item {
  margin-right: 12px;
}

.category-label {
  @include variables.headings-font();
  font-size: 24px;
}
</style>
