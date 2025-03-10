<template>
  <SidebarSection>
    <h2>Links</h2>

    <SidebarList>
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
    </SidebarList>
  </SidebarSection>
</template>

<script>
import FontAwesomeCircleIcon from "./FontAwesomeCircleIcon";
import SidebarSocialItem from "./SidebarSocialItem.vue";
import SidebarSection from "./SidebarSection";
import SidebarList from "@/components/navlink/SidebarList.vue";

export default {
  name: "SidebarSocialList",
  components: {
    SidebarList,
    SidebarSection,
    FontAwesomeCircleIcon,
    SidebarSocialItem,
  },
};
</script>
