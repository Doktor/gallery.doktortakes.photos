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

      <SidebarList class="sidebar-items">
        <!-- Main links -->
        <SidebarSection>
          <h2>Albums</h2>

          <SidebarList>
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
          </SidebarList>
        </SidebarSection>

        <!-- Content management -->
        <SidebarSection v-if="isStaff">
          <h2>Manage</h2>

          <SidebarList>
            <SidebarLink title="Dashboard" route="manage" />
            <SidebarListItem>
              <a class="sidebar-link" href="/admin/">Admin</a>
            </SidebarListItem>
            <SidebarLink title="Groups" route="groups" />
            <SidebarLink title="Users" route="users" />
          </SidebarList>
        </SidebarSection>

        <!-- User management -->
        <SidebarSection>
          <h2>User</h2>

          <SidebarList>
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
          </SidebarList>
        </SidebarSection>

        <SidebarDivider />

        <SidebarSocialSection />

        <SidebarDivider />
      </SidebarList>

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
import SidebarList from "./SidebarList";
import SidebarSection from "./SidebarSection";
import SidebarListItem from "./SidebarListItem";
import CustomButton from "@/components/form/CustomButton";
import SidebarMenu from "./SidebarMenu";
import SidebarMenuButton from "./SidebarMenuButton";

export default {
  components: {
    SidebarMenuButton,
    SidebarMenu,
    CustomButton,
    SidebarListItem,
    SidebarSection,
    SidebarList,
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
  text-align: left;
  width: variables.$sidebar-width;

  margin: 0 auto 2rem auto;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    margin: 0;
  }

  h2 {
    font-size: 2rem;

    margin: 0;
    margin-bottom: 16px;
  }
}

.sidebar-items {
  @include variables.headings-font();
  font-size: 1.5rem;
  text-transform: lowercase;
}

@mixin link($text-color, $background-color: variables.$background-color) {
  color: $text-color;
  background-color: $background-color;

  &:hover {
    color: $background-color;
    background-color: $text-color;
  }
}

.sidebar-link {
  display: inline-block;
  padding: variables.$sidebar-link-margin;
  padding-left: variables.$sidebar-link-margin * 3;
  width: 100%;

  text-decoration-line: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 4px;

  transition: color, background-color;

  @include link(variables.$text-color);

  .sidebar-item-profile & {
    @include link(variables.$text-blue);
  }

  .sidebar-item-log-out & {
    @include link(variables.$text-error);
  }
}
</style>
