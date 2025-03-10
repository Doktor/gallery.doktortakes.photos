<template>
  <nav class="nav nav-index">
    <ul class="nav-items">
      <!-- Main links -->
      <Navlink title="Albums" display="Photos" route="albums" />
      <Navlink title="About" route="about" />

      <!-- Content management -->
      <Navlink v-if="isStaff" title="Edit" route="manage" />

      <!-- User management -->
      <Navlink
        v-if="isAuthenticated"
        class="nav-item-log-out"
        title="Log out"
        route="logOut"
      />
      <Navlink v-else title="Log in" route="logIn" />
    </ul>
  </nav>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import Navlink from "./Navlink";

export default {
  name: "IndexNavlinks",
  components: {
    Navlink,
  },
  computed: {
    ...mapGetters(["isAuthenticated", "isStaff"]),
    ...mapState(["user"]),
  },
};
</script>

<style lang="scss">
.nav-index {
  padding: 0;
  margin: 0;
}

.nav-index .nav-item-link {
  color: variables.$background-color;
  line-height: 1;

  &:hover {
    text-decoration: underline;
  }

  @media (min-width: 901px) {
    font-size: variables.$nav-font-size-index;
  }
}
</style>
