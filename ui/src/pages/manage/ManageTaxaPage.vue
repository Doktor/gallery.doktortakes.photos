<template>
  <div>
    <form>
      <CustomInput
        label="Catalogue of Life identifier"
        v-model="catalogId"
        maxlength="10"
      />
      <CustomButton @click="submit">Add</CustomButton>
    </form>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Rank</th>
          <th>Name</th>
          <th>Common name</th>
          <th>Created date</th>
          <th>Updated date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="taxon in taxa" :key="taxon.id">
          <td>{{ taxon.catalog_id }}</td>
          <td>{{ taxon.rank }}</td>
          <td>{{ taxon.name }}</td>
          <td>{{ taxon.common_name }}</td>
          <td>{{ formatDateTime(taxon.created_date) }}</td>
          <td>{{ formatDateTime(taxon.updated_date) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { TaxaService } from "@/services/TaxaService";
import CustomInput from "@/components/form/CustomInput";
import CustomButton from "@/components/form/CustomButton";
import { postAsync } from "@/utils";
import { formatDateTime } from "@/date";

export default {
  components: { CustomButton, CustomInput },

  data() {
    return {
      catalogId: "",
      taxa: [],
      loading: true,
    };
  },

  async created() {
    this.loading = true;
    this.taxa = await TaxaService.getTaxa();
    this.loading = false;
  },

  methods: {
    formatDateTime,

    async submit() {
      let { ok, content } = await postAsync("/api/manage/taxa/import/", {
        catalogId: this.catalogId,
      });

      if (!ok) {
        this.$store.commit("addNotification", {
          message: `An error occurred when importing this taxon: ${content}`,
          status: "error",
        });

        return;
      }

      this.$store.commit("addNotification", {
        message: "Succesfully imported taxon.",
        status: "success",
      });

      // TODO: refresh list
    },
  },
};
</script>

<style scoped>
form {
  display: grid;
}
</style>
