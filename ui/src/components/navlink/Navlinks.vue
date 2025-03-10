<template>
  <nav v-if="showNav" class="nav">
    <NavlinksHeader />

    <ul class="nav-items">
      <li class="nav-section">
        <h2>
          <a href="https://doktortakes.photos/about/">About</a>
        </h2>
      </li>

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

      <!-- Social media links -->
      <li class="nav-section">
        <h2>Social</h2>

        <div class="nav-socials">
          <!-- Twitter -->
          <NavlinkSocial
            href="https://twitter.com/DoktorTheHusky"
            title="Twitter"
          >
            <FontAwesomeCircleIcon iconClass="fab fa-twitter" />
          </NavlinkSocial>

          <!-- Telegram -->
          <NavlinkSocial href="https://t.me/DoktorTakesPhotos" title="Telegram">
            <i class="fab fa-telegram"></i>
          </NavlinkSocial>

          <!-- Website -->
          <NavlinkSocial href="https://doktorthehusky.com" title="Website">
            <i class="fas fa-globe-americas"></i>
          </NavlinkSocial>
        </div>
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
    </ul>

    <NavFooter />
  </nav>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import Navlink from "./Navlink";
import NavlinkSocial from "./NavlinkSocial";
import FontAwesomeCircleIcon from "./FontAwesomeCircleIcon";
import NavlinksHeader from "./NavlinksHeader";
import NavFooter from "@/components/navlink/NavFooter.vue";

export default {
  components: {
    NavFooter,
    NavlinksHeader,
    FontAwesomeCircleIcon,
    NavlinkSocial,
    Navlink,
  },
  computed: {
    ...mapGetters(["isAuthenticated", "isStaff"]),
    ...mapState(["showNav", "user"]),
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

    text-decoration-line: underline;
    text-decoration-color: variables.$text-color-2;
    text-decoration-thickness: 1px;
    text-underline-offset: 4px;
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

  margin-bottom: 12px;

  &::before {
    content: "-";
    color: variables.$text-color-2;
    font-size: 1rem;
    font-weight: 700;

    margin-right: 6px;
  }
}

.nav-socials {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}

.nav-item-link {
  .nav-item-profile & {
    color: variables.$text-blue;
  }

  .nav-item-log-out & {
    color: variables.$text-error;
  }
}
</style>
