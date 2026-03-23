<template>
  <header class="sidebar-header">
    <h1 class="sidebar-logo">
      <router-link
        class="sidebar-logo-link"
        title="Doktor & Associates LLP"
        @click="onClick"
        :to="{ name: 'index' }"
      >
        <div class="logo-name">Doktor</div>
        <div class="logo-subtitle">& Associates LLP</div>

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
    " + Associates LLP"
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
  color: #0078ff;
  font-size: 60px;
}

.logo-subtitle {
  color: #333333;
  font-size: 24px;
}

.logo-bar {
  margin-top: 8px;

  div {
    height: 12px;
  }
}
</style>
