<template>
  <nav v-if="showNavigation" class="nav">
    <SidebarHeader />

    <SidebarList class="nav-items">
      <!-- Main links -->
      <SidebarSection>
        <h2>Albums</h2>

        <SidebarList>
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
        </SidebarList>
      </SidebarSection>

      <!-- Content management -->
      <SidebarSection v-if="isStaff">
        <h2>Manage</h2>

        <SidebarList>
          <Navlink title="Dashboard" route="manage" />
          <li class="nav-item">
            <a class="nav-item-link" href="/admin/">Admin</a>
          </li>
          <Navlink title="Groups" route="groups" />
          <Navlink title="Users" route="users" />
        </SidebarList>
      </SidebarSection>

      <!-- User management -->
      <SidebarSection v-if="isAuthenticated">
        <h2>User</h2>

        <SidebarList>
          <Navlink
            class="nav-item-profile"
            title="Profile"
            :to="{ name: 'user', params: { slug: user.name } }"
          />
          <Navlink class="nav-item-log-out" title="Log out" route="logOut" />
        </SidebarList>
      </SidebarSection>
      <Navlink v-else-if="!isAuthenticated" title="Log in" route="logIn" />

      <SidebarDivider />

      <!-- About -->
      <SidebarSection>
        <h2>
          <a href="https://doktortakes.photos/about/">About</a>
        </h2>
      </SidebarSection>

      <SidebarSocials />

      <SidebarDivider />
    </SidebarList>

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
import SidebarList from "./SidebarList";
import SidebarSection from "./SidebarSection";

export default {
  components: {
    SidebarSection,
    SidebarList,
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
