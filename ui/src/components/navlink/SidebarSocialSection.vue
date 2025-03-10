<template>
  <SidebarSection>
    <h2>Links</h2>

    <div class="test">
      <SidebarSocialItem
        href="https://doktortakes.photos/about/"
        title="About me"
      >
        <i class="fas fa-info-circle"></i>
      </SidebarSocialItem>

      <SidebarSocialItem href="mailto:doktorthehusky@gmail.com" title="Email">
        <FontAwesomeCircleIcon iconClass="fas fa-envelope" />
      </SidebarSocialItem>

      <!-- Twitter -->
      <SidebarSocialItem
        href="https://twitter.com/DoktorTheHusky"
        title="Twitter"
      >
        <FontAwesomeCircleIcon iconClass="fab fa-twitter" />
      </SidebarSocialItem>

      <!-- Telegram -->
      <SidebarSocialItem href="https://t.me/DoktorTakesPhotos" title="Telegram">
        <i class="fab fa-telegram"></i>
      </SidebarSocialItem>

      <!-- Website -->
      <SidebarSocialItem href="https://doktorthehusky.com" title="Website">
        <i class="fas fa-globe-americas"></i>
      </SidebarSocialItem>
    </div>
  </SidebarSection>
</template>

<script>
import FontAwesomeCircleIcon from "./FontAwesomeCircleIcon";
import SidebarSocialItem from "./SidebarSocialItem.vue";
import SidebarSection from "./SidebarSection";
import SidebarList from "@/components/navlink/SidebarList.vue";

export default {
  name: "SidebarSocialSection",
  components: {
    SidebarList,
    SidebarSection,
    FontAwesomeCircleIcon,
    SidebarSocialItem,
  },
};
</script>

<style lang="scss">
.test {
  display: grid;
}
</style>
