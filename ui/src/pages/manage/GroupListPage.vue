<template>
  <FixedWidthContainer>
    <h2>Groups</h2>

    <table v-if="!loading">
      <thead>
        <tr>
          <th>ID</th>
          <th class="group-name">Name</th>
          <th>Users</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(group, index) in groups" :key="index">
          <td>{{ group.id }}</td>
          <td class="group-name">{{ group.name }}</td>
          <td>{{ formatUsers(group.users) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else>Loading...</p>
  </FixedWidthContainer>
</template>

<script>
import { mapState } from "pinia";
import { useStore } from "@/store";
import FixedWidthContainer from "@/components/FixedWidthContainer";
import { ManageUserService } from "@/services/manage/ManageUserService";

export default {
  components: {
    FixedWidthContainer,
  },

  computed: {
    ...mapState(useStore, ["loading"]),
  },

  data() {
    return {
      groups: [],
    };
  },

  async created() {
    const store = useStore();
    store.setBreadcrumbs([
      { label: "Manage", to: { name: "manage" } },
      { label: "Groups", to: { name: "groups" } },
    ]);
    store.setLoading(true);
    this.groups = await ManageUserService.listGroups();
    store.setLoading(false);
  },

  methods: {
    formatUsers(users) {
      return users
        .slice()
        .sort((a, b) => a.localeCompare(b))
        .join(", ");
    },
  },
};
</script>

<style scoped lang="scss">
.group-name {
  white-space: nowrap;
}
</style>
