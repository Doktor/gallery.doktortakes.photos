<template>
  <nav class="sidebar">
    <SidebarHeader />

    <CustomButton
      class="sidebar-menu-button open-menu-button"
      @click="isMenuOpen = true"
    >
      <MenuIcon class="menu-icon" /><span>Menu</span>
    </CustomButton>

    <SidebarMenu :isOpen="isMenuOpen">
      <CustomButton
        class="sidebar-menu-button close-menu-button"
        @click="isMenuOpen = false"
      >
        <span>&times; Close</span>
      </CustomButton>

      <SidebarList class="sidebar-items">
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
            <SidebarListItem>
              <a class="sidebar-link" href="/admin/">Admin</a>
            </SidebarListItem>
            <Navlink title="Groups" route="groups" />
            <Navlink title="Users" route="users" />
          </SidebarList>
        </SidebarSection>

        <!-- User management -->
        <SidebarSection>
          <h2>User</h2>

          <SidebarList>
            <Navlink
              v-if="isAuthenticated"
              class="sidebar-item-profile"
              title="Profile"
              :to="{ name: 'user', params: { slug: user.name } }"
            />
            <Navlink
              v-if="isAuthenticated"
              class="sidebar-item-log-out"
              title="Log out"
              route="logOut"
            />
            <Navlink
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
import Navlink from "./Navlink";
import SidebarHeader from "./SidebarHeader";
import SidebarFooter from "./SidebarFooter";
import SidebarDivider from "@/components/navlink/SidebarDivider.vue";
import SidebarSocialSection from "./SidebarSocialSection";
import SidebarList from "./SidebarList";
import SidebarSection from "./SidebarSection";
import SidebarListItem from "./SidebarListItem";
import CustomButton from "@/components/form/CustomButton.vue";
import SidebarMenu from "@/components/navlink/SidebarMenu.vue";
import MenuIcon from "@/components/navlink/MenuIcon.vue";

export default {
  components: {
    MenuIcon,
    SidebarMenu,
    CustomButton,
    SidebarListItem,
    SidebarSection,
    SidebarList,
    SidebarSocialSection,
    SidebarDivider,
    SidebarFooter,
    SidebarHeader,
    Navlink,
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

.sidebar-menu-button {
  background: none;
  width: variables.$sidebar-width;

  border: 1px solid black;
  border-radius: 2px;
  margin: 0 auto;
  margin-bottom: variables.$sidebar-margin;
  padding: 12px;

  cursor: pointer;

  @include variables.headings-font();
  font-size: 2rem;
  text-transform: uppercase;

  &:hover {
    background-color: rgb(230, 230, 230);
  }

  &,
  &:hover {
    transition: background-color 0.1s ease-in-out;
  }
}

.open-menu-button {
  display: inline-flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: none;
  }

  .menu-icon {
    width: 1rem;
    height: 1rem;

    margin-right: 12px;
  }
}

.close-menu-button {
  @media (width >= variables.$full-layout-breakpoint + 1) {
    display: none;
  }
}
</style>
