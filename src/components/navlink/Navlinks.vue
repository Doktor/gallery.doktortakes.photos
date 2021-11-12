<template>
  <nav v-if="showNav" class="nav">
    <ul class="nav-items">
      <template v-if="showLogo">
        <NavlinksLogo />
        <NavlinkDivider v-if="showDividers" />
      </template>

      <!-- Main links -->
      <Navlink title="Featured" route="featured" />

      <NavlinkMenu title="Photos">
        <Navlink title="Archive" display="Archive" route="albums" />
        <Navlink
          v-if="user.status !== 'anonymous'"
          title="Your albums"
          :to="{ name: 'user', params: { slug: user.name } }"
        />
        <Navlink title="Tags" route="tags" />
        <Navlink title="Search" route="search" />
      </NavlinkMenu>

      <Navlink title="About" route="about" />

      <!-- Social media links -->
      <template v-if="!isStaff">
        <NavlinkDivider v-if="showDividers" />

        <!-- Twitter -->
        <NavlinkSocial
          href="https://twitter.com/DoktorTheHusky"
          title="Twitter"
        >
          <FontAwesomeCircleIcon iconClass="fab fa-twitter"/>
        </NavlinkSocial>

        <!-- Telegram -->
        <NavlinkSocial href="https://t.me/DoktorTakesPhotos" title="Telegram">
          <i class="fab fa-telegram"></i>
        </NavlinkSocial>

        <!-- Website -->
        <NavlinkSocial href="https://doktorthehusky.com" title="Website">
          <i class="fas fa-globe-americas"></i>
        </NavlinkSocial>
      </template>

      <!-- Content management -->
      <NavlinkDivider v-if="showDividers" />
      <template v-if="isStaff">
        <li class="nav-item">
          <a class="nav-item-link" href="/admin/">Admin</a>
        </li>
        <Navlink title="Manage" route="manage" />
      </template>

      <!-- User management -->
      <template v-if="isAuthenticated">
        <Navlink
          class="nav-item-profile"
          title="Profile"
          :to="{ name: 'user', params: { slug: user.name } }"
        />
        <Navlink class="nav-item-log-out" title="Log out" route="logOut" />
      </template>
      <Navlink
        v-else-if="!isAuthenticated"
        title="Log in"
        route="logIn"
      />
    </ul>
  </nav>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import Navlink from "@/components/navlink/Navlink.vue";
import NavlinkDivider from "@/components/navlink/NavlinkDivider.vue";
import NavlinkSocial from "@/components/navlink/NavlinkSocial.vue";
import NavlinksLogo from "@/components/navlink/NavlinksLogo.vue";
import NavlinkMenu from "@/components/navlink/NavlinkMenu.vue";
import FontAwesomeCircleIcon from "@/components/navlink/FontAwesomeCircleIcon.vue";

export default {
  components: {
    FontAwesomeCircleIcon,
    NavlinkMenu,
    NavlinksLogo,
    NavlinkSocial,
    NavlinkDivider,
    Navlink,
  },
  computed: {
    ...mapGetters(["isAuthenticated", "isStaff"]),
    ...mapState(["showNav", "user"]),
  },

  props: {
    showDividers: {
      type: Boolean,
      default: true,
    },
    showLogo: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style lang="scss">
.nav {
  margin: 0;
  margin-top: 1.5rem;
  padding: 0;
}

.nav-items {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;

  @include headings-font();
  font-size: $nav-font-size;
  text-transform: lowercase;

  padding: 0;
  margin: 0;

  list-style: none;
}

.nav-index .nav-items {
  @media (min-width: 601px) {
    justify-content: flex-start;
  }
}

.nav-item {
  display: block;

  margin: 0 ($nav-item-spacing / 2);
  margin-bottom: 1rem;

  @media (min-width: 901px) {
    line-height: $nav-logo-size * 1.15;
  }
}

.nav-index .nav-item {
  line-height: 1;
  margin-bottom: 0;

  &:first-child {
    margin-left: 0;
  }

  &:last-child {
    margin-right: 0;
  }
}

.nav-item-link {
  color: $text-color;

  .nav-item-profile & {
    color: $text-blue;
  }

  .nav-item-log-out & {
    color: $text-error;
  }
}
</style>
