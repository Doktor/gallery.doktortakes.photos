<template>
  <nav class="sidebar">
    <SidebarHeader />

    <SidebarMenuButton
      @click="isMenuOpen = true"
      iconClass="fas fa-caret-square-down"
      title="Menu"
    />

    <SidebarMenu :isOpen="isMenuOpen">
      <SidebarMenuButton
        @click="isMenuOpen = false"
        iconClass="fas fa-times"
        title="Close"
      />

      <ul class="sidebar-items">
        <!-- Main links -->
        <li class="sidebar-section">
          <h2>Albums</h2>

          <ul>
            <SidebarLink title="All albums" route="index" />
            <SidebarLink
              v-if="user.status !== 'anonymous'"
              title="Your albums"
              :to="{ name: 'user', params: { slug: user.name } }"
            />
            <SidebarLink title="Tags" route="tags" />
            <!-- <SidebarLink title="Taxonomy" route="taxa" />-->
            <!-- <SidebarLink title="Species" route="species" />-->
            <SidebarLink title="Search" route="search" />
          </ul>
        </li>

        <!-- Content management -->
        <li class="sidebar-section" v-if="isStaff">
          <h2>Manage</h2>

          <ul>
            <SidebarLink title="Dashboard" route="manage" />
            <SidebarLink title="Admin" href="/admin/" />
            <SidebarLink title="Groups" route="groups" />
            <SidebarLink title="Users" route="users" />
          </ul>
        </li>

        <!-- User management -->
        <li class="sidebar-section">
          <h2>User</h2>

          <ul>
            <SidebarLink
              v-if="isAuthenticated"
              class="sidebar-item-profile"
              title="Profile"
              :to="{ name: 'user', params: { slug: user.name } }"
            />
            <SidebarLink
              v-if="isAuthenticated"
              class="sidebar-item-log-out"
              title="Log out"
              route="logOut"
            />
            <SidebarLink
              v-if="!isAuthenticated"
              class="sidebar-item-profile"
              title="Log in"
              route="logIn"
            />
          </ul>
        </li>

        <SidebarDivider />

        <SidebarSocialSection />

        <SidebarDivider />
      </ul>

      <SidebarFooter />
    </SidebarMenu>
  </nav>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import SidebarLink from "./SidebarLink";
import SidebarHeader from "./SidebarHeader";
import SidebarFooter from "./SidebarFooter";
import SidebarDivider from "./SidebarDivider";
import SidebarSocialSection from "./SidebarSocialSection";
import CustomButton from "@/components/form/CustomButton";
import SidebarMenu from "./SidebarMenu";
import SidebarMenuButton from "./SidebarMenuButton";

export default {
  components: {
    SidebarMenuButton,
    SidebarMenu,
    CustomButton,
    SidebarSocialSection,
    SidebarDivider,
    SidebarFooter,
    SidebarHeader,
    SidebarLink,
  },
  computed: {
    ...mapGetters(["isAuthenticated", "isStaff"]),
    ...mapState(["user"]),
  },

  data() {
    return {
      isMenuOpen: false,
    };
  },

  methods: {},
};
</script>

<style lang="scss">
.sidebar {
  @include variables.sidebar-font();
  font-size: 1.3rem;
  text-align: left;

  width: variables.$sidebar-width;

  margin: 0 auto 2rem auto;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    margin: 0;
  }

  h2 {
    font-size: 2rem;
  }

  ul {
    margin: 0;
    padding: 0;

    list-style-type: none;
  }
}

.sidebar-items {
  text-transform: lowercase;
}

.sidebar-section {
  margin-bottom: variables.$sidebar-margin;
}
</style>
