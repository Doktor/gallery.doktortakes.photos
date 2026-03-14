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
        <!-- Featured albums -->
        <li class="sidebar-section" v-if="featuredAlbums.length">
          <h2
            class="sidebar-featured-toggle"
            @click="isFeaturedOpen = !isFeaturedOpen"
            title="Click to expand"
          >
            <i
              class="fas fa-chevron-right sidebar-featured-arrow"
              :class="{ 'sidebar-featured-arrow-open': isFeaturedOpen }"
            />
            Featured
          </h2>

          <SidebarAlbumTree
            v-show="isFeaturedOpen"
            class="sidebar-featured-tree"
            :items="albumTree"
          />
        </li>

        <!-- Main links -->
        <li class="sidebar-section">
          <h2>Photos</h2>

          <ul>
            <SidebarLink title="Albums" route="index" />
            <SidebarLink title="Tags" route="tags" />
            <!-- <SidebarLink title="Taxonomy" route="taxa" />-->
            <!-- <SidebarLink title="Species" route="species" />-->
            <!-- <SidebarLink title="Search" route="search" />-->
          </ul>
        </li>

        <!-- Content management -->
        <li class="sidebar-section" v-if="isStaff">
          <h2>Manage</h2>

          <ul>
            <SidebarLink title="Dashboard" route="manage" />
            <SidebarLink title="Groups" route="groups" />
            <SidebarLink title="Users" route="users" />
            <SidebarLink title="Admin" href="/admin/" />
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
import { AlbumService } from "@/services/AlbumService";
import SidebarTree from "./SidebarTree.vue";
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
    SidebarAlbumTree: SidebarTree,
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

    albumTree() {
      const albumsByPath = new Map();
      const topLevel = [];

      const albums = this.featuredAlbums.sort((a, b) =>
        a.name.localeCompare(b.name),
      );

      for (const album of albums) {
        albumsByPath.set(album.path, { album, children: [] });
      }

      for (const album of albums) {
        const parentPath = album.path.includes("/")
          ? album.path.slice(0, album.path.lastIndexOf("/"))
          : null;

        if (parentPath === null) {
          topLevel.push(albumsByPath.get(album.path));
        } else {
          const parent = albumsByPath.get(parentPath);
          parent.children.push(albumsByPath.get(album.path));
        }
      }

      return topLevel;
    },
  },

  data() {
    return {
      isMenuOpen: false,
      isFeaturedOpen: false,
      featuredAlbums: [],
    };
  },

  async created() {
    this.featuredAlbums = await AlbumService.getFeaturedAlbums();
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

.sidebar-featured-tree {
  background-color: variables.$background-color-2;
  padding: 16px !important;
}

.sidebar-featured-toggle {
  display: flex;
  align-items: center;
  gap: 12px;

  cursor: pointer;
  user-select: none;
}

.sidebar-featured-arrow {
  font-size: 16px;

  &.sidebar-featured-arrow-open {
    transform: rotate(90deg);
  }
}
</style>
