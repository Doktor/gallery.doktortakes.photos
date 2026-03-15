<template>
  <header class="sidebar-header">
    <h1 class="sidebar-logo">
      <router-link
        class="sidebar-logo-link"
        :title="title"
        @click="onClick"
        :to="{ name: 'index' }"
      >
        <div v-for="associate in associates" class="logo-name">
          <span :style="`color: ${associate.color}`">{{ associate.name }}</span>
          <span class="logo-gray-text">+</span>
        </div>

        <div class="logo-subtitle">
          <div class="logo-gray-text logo-small-text">Associates</div>
          <div class="logo-gray-text logo-small-text">GmbH</div>
        </div>

        <div class="logo-bar">
          <div
            v-for="associate in associates"
            :style="`background-color: ${associate.color} `"
          />
        </div>
      </router-link>
    </h1>
  </header>
</template>

<script setup>
import { shuffleArray } from "@/utils";
import { computed, reactive } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const associates = reactive([
  {
    name: "Doktor",
    color: "#0078ff",
  },
  {
    name: "Archer",
    color: "#ff0000",
  },
  {
    name: "Baxter",
    color: "#ff9900",
  },
]);

const title = computed(() => {
  return (
    associates.map((associate) => associate.name).join(" + ") +
    " Associates GmbH"
  );
});

function onClick() {
  if (route.name === "index") {
    const oldTitle = title.value;

    while (true) {
      shuffleArray(associates);

      if (oldTitle !== title.value) {
        break;
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar-header {
  margin-bottom: variables.$sidebar-margin;
}

.sidebar-logo {
  @include variables.logo-font();
  text-align: left;

  margin: 0;
  padding: 0;

  user-select: none;
}

.sidebar-logo-link {
  text-decoration: none;
}

.logo-name {
  display: flex;
  justify-content: space-between;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    font-size: 48px;
  }
}

.logo-subtitle {
  margin-top: 4px;
}

.logo-gray-text {
  color: #333333;
}

.logo-small-text {
  font-size: 36px;
  margin-bottom: 8px;
}

.logo-bar {
  margin-top: 8px;

  div {
    height: 12px;
  }
}
</style>
