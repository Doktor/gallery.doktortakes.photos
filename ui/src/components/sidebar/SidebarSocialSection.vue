<template>
  <li class="sidebar-section">
    <h2>Links</h2>

    <ul>
      <SidebarSocialLink
        href="https://doktortakes.photos/about/"
        title="About me"
      >
        <i class="fas fa-info-circle"></i>
      </SidebarSocialLink>

      <SidebarSocialLink href="mailto:doktorthehusky@gmail.com" title="Email">
        <FontAwesomeCircleIcon iconClass="fas fa-envelope" />
      </SidebarSocialLink>

      <!-- Twitter -->
      <SidebarSocialLink
        href="https://twitter.com/DoktorTheHusky"
        title="Twitter"
      >
        <FontAwesomeCircleIcon iconClass="fab fa-twitter" />
      </SidebarSocialLink>

      <!-- Telegram -->
      <SidebarSocialLink href="https://t.me/DoktorTakesPhotos" title="Telegram">
        <i class="fab fa-telegram"></i>
      </SidebarSocialLink>

      <!-- Website -->
      <SidebarSocialLink href="https://doktorthehusky.com" title="Website">
        <i class="fas fa-globe-americas"></i>
      </SidebarSocialLink>
    </ul>
  </li>
</template>

<script>
import FontAwesomeCircleIcon from "./FontAwesomeCircleIcon";
import SidebarSocialLink from "./SidebarSocialLink.vue";

export default {
  name: "SidebarSocialSection",
  components: {
    FontAwesomeCircleIcon,
    SidebarSocialLink,
  },
};
</script>
