<template>
  <nav v-if="showNavigation" class="nav">
    <SidebarHeader />

    <ul class="nav-items">
      <!-- Main links -->
      <li class="nav-section">
        <h2>Albums</h2>

        <ul>
          <Navlink title="All albums" route="index" />
          <Navlink
            v-if="user.status !== 'anonymous'"
            title="Your albums"
            :to="{ name: 'user', params: { slug: user.name } }"
          />
          <Navlink title="Tags" route="tags" />
          <!-- <Navlink title="Taxonomy" route="taxa" />-->
          <!-- <Navlink title="Species" route="species" />-->
          <Navlink title="Search" route="search" />
        </ul>
      </li>

      <!-- Content management -->
      <li v-if="isStaff" class="nav-section">
        <h2>Manage</h2>

        <ul>
          <Navlink title="Dashboard" route="manage" />
          <li class="nav-item">
            <a class="nav-item-link" href="/admin/">Admin</a>
          </li>
          <Navlink title="Groups" route="groups" />
          <Navlink title="Users" route="users" />
        </ul>
      </li>

      <!-- User management -->
      <li v-if="isAuthenticated" class="nav-section">
        <h2>User</h2>

        <ul>
          <Navlink
            class="nav-item-profile"
            title="Profile"
            :to="{ name: 'user', params: { slug: user.name } }"
          />
          <Navlink class="nav-item-log-out" title="Log out" route="logOut" />
        </ul>
      </li>
      <Navlink v-else-if="!isAuthenticated" title="Log in" route="logIn" />

      <SidebarDivider />

      <!-- About -->
      <li class="nav-section">
        <h2>
          <a href="https://doktortakes.photos/about/">About</a>
        </h2>
      </li>

      <SidebarSocials />

      <SidebarDivider />
    </ul>

    <SidebarFooter />
  </nav>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import Navlink from "./Navlink";
import SidebarHeader from "./SidebarHeader";
import SidebarFooter from "./SidebarFooter";
import SidebarDivider from "@/components/navlink/SidebarDivider.vue";
import SidebarSocials from "@/components/navlink/SidebarSocials.vue";

export default {
  components: {
    SidebarSocials,
    SidebarDivider,
    SidebarFooter,
    SidebarHeader,
    Navlink,
  },
  computed: {
    ...mapGetters(["isAuthenticated", "isStaff"]),
    ...mapState(["showNavigation", "user"]),
  },
};
</script>

<style lang="scss">
ul {
  margin: 0;
  padding: 0;
}

.nav {
  margin: 0;
  padding: 0;

  text-align: left;

  width: variables.$sidebar-width;

  h2 {
    font-size: 2rem;
    line-height: 1;

    margin: 0;
    margin-bottom: 24px;
  }
}

.nav-items {
  @include variables.headings-font();
  font-size: variables.$nav-font-size;
  text-transform: lowercase;

  padding: 0;
  margin: 0;

  &,
  ul {
    list-style-type: none;
  }

  a,
  h2 a {
    color: variables.$text-color;

    padding: 6px;

    text-decoration-line: underline;
    text-decoration-thickness: 1px;
    text-underline-offset: 4px;

    transition: color, background-color;
  }

  a:hover,
  h2 a:hover {
    color: variables.$background-color;
    background-color: variables.$text-color;
  }
}

.nav-section {
  margin-bottom: 40px;
}

.nav-item {
  display: block;

  font-size: 1.2rem;
  font-weight: 400;
  line-height: 1;

  &::before {
    content: "-";
    color: variables.$text-color;
    font-size: 1rem;
    font-weight: 400;

    margin-right: 2px;
  }
}

.nav-item-link {
  display: inline-block;

  .nav-item-profile & {
    color: variables.$text-blue;
  }

  .nav-item-log-out & {
    color: variables.$text-error;
  }
}
</style>
