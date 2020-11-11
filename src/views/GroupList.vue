<template>
  <FixedWidthContainer>
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
import {mapState} from 'vuex';
import FixedWidthContainer from "../components/FixedWidthContainer.vue";


export default {
  components: {
    FixedWidthContainer,
  },

  computed: {
    ...mapState([
      'loading',
      'groups',
    ]),
  },

  created() {
    this.$store.dispatch('getGroups');
  },

  methods: {
    formatUsers(users) {
      return users.slice().sort((a, b) => a.localeCompare(b)).join(', ');
    },
  },
}
</script>

<style scoped>
table {
  margin: 0 auto;
}

thead {
  background-color: rgb(60, 60, 60);
  text-align: center;
}

th, td {
  padding: 4px 8px;
}

tr:nth-child(even) {
  background-color: rgb(40, 40, 40);
}

.group-name {
  white-space: nowrap;
}
</style>
