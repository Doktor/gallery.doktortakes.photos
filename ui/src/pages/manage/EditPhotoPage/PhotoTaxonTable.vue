<template>
  <table>
    <thead>
      <tr>
        <th>Catalog ID</th>
        <th>Name</th>
        <th>Common name</th>
        <th>Rating</th>
        <th>Notes</th>
        <th></th>
      </tr>
    </thead>

    <tbody>
      <tr
        v-for="taxon in editingTaxa"
        :key="taxon.catalogId"
        :class="getRowClasses(taxon)"
      >
        <td>{{ taxon.catalogId }}</td>
        <td>{{ taxon.name }}</td>
        <td>{{ taxon.commonName }}</td>
        <td>
          <CustomInput
            label=""
            type="number"
            v-model="taxon.rating"
            min="0"
            max="5"
            default="0"
            @input="markUpdated(taxon)"
          />
        </td>
        <td>
          <CustomInput
            label=""
            v-model="taxon.notes"
            @input="markUpdated(taxon)"
          />
        </td>
        <td>
          <CustomButton @click="toggleDeleteTaxon(taxon)">
            <template v-if="taxon.status === 'delete'">Keep</template>
            <template v-else>Delete</template>
          </CustomButton>
        </td>
      </tr>

      <tr>
        <td>Add taxon</td>
        <td colspan="5">
          <CustomInput label="" v-model="searchText" />

          <div class="search-results">
            <ul>
              <li class="search-results-header">
                Search results ({{ searchResults.length }})
              </li>
              <li
                v-for="taxon in searchResults.slice(0, this.searchResultsLimit)"
                :key="taxon.catalogId"
                class="search-result"
                @click="addTaxon(taxon)"
              >
                {{ taxon.commonName }} ({{ taxon.name }})
              </li>
              <li v-if="searchResults.length > searchResultsLimit" class="note">
                {{ searchResults.length - searchResultsLimit }} result(s) hidden
              </li>
            </ul>
          </div>
        </td>
      </tr>

      <tr>
        <td colspan="5"></td>
        <td><CustomButton @click="save">Save</CustomButton></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { useStore } from "@/store";
import CustomInput from "@/components/form/CustomInput.vue";
import { TaxaService } from "@/services/TaxaService";
import CustomButton from "@/components/form/CustomButton.vue";
import { ManagePhotoTaxonService } from "@/services/manage/ManagePhotoTaxonService";

const STATUS_KEEP = "keep";
const STATUS_CREATE = "create";
const STATUS_UPDATE = "update";
const STATUS_DELETE = "delete";

export default {
  components: { CustomButton, CustomInput },
  props: {
    photo: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      loading: true,
      searchText: "",

      editingTaxa: [],

      allSpecies: [],
      searchResults: [],
      searchResultsLimit: 5,
    };
  },

  async mounted() {
    this.loading = true;

    for (let taxon of this.photo.taxa) {
      this.editingTaxa.push({ ...taxon, status: STATUS_KEEP });
    }

    let taxa = await TaxaService.getTaxa();
    this.allSpecies = taxa.filter((taxon) => taxon.rank === "species");

    this.loading = false;
  },

  methods: {
    addTaxon(taxon) {
      this.editingTaxa.push({ ...taxon, status: STATUS_CREATE });
    },

    markUpdated(taxon) {
      if (taxon.status === STATUS_KEEP) {
        taxon.status = STATUS_UPDATE;
      }
    },

    toggleDeleteTaxon(taxon) {
      switch (taxon.status) {
        case STATUS_CREATE:
          this.editingTaxa.splice(this.editingTaxa.indexOf(taxon));
          break;
        case STATUS_KEEP:
          taxon.status = STATUS_DELETE;
          break;
        case STATUS_DELETE:
          taxon.status = STATUS_KEEP;
          break;
      }
    },

    getRowClasses(taxon) {
      let value = {};

      switch (taxon.status) {
        case STATUS_CREATE:
          value["row-create"] = true;
          break;

        case STATUS_DELETE:
          value["row-delete"] = true;
          break;

        case STATUS_UPDATE:
          value["row-update"] = true;
          break;
      }

      return value;
    },

    async save() {
      const store = useStore();
      let toCreate = this.editingTaxa.filter((t) => t.status === STATUS_CREATE);
      let toUpdate = this.editingTaxa.filter((t) => t.status === STATUS_UPDATE);
      let toDelete = this.editingTaxa.filter((t) => t.status === STATUS_DELETE);

      for (let taxon of toCreate) {
        let { ok, content } = await ManagePhotoTaxonService.create(
          this.photo.md5,
          {
            taxon: taxon.catalogId,
            rating: taxon.rating,
            notes: taxon.notes,
          },
        );

        if (!ok) {
          store.addNotification({
            message: "An error occurred when creating a taxon link.",
            status: "error",
          });
        }

        this.editingTaxa[this.editingTaxa.indexOf(taxon)] = content;
      }

      for (let taxon of toUpdate) {
        let { ok, content } = await ManagePhotoTaxonService.update(
          this.photo.md5,
          taxon.catalogId,
          {
            taxon: taxon.catalogId,
            rating: taxon.rating,
            notes: taxon.notes,
          },
        );

        if (!ok) {
          store.addNotification({
            message: "An error occurred when updating a taxon link.",
            status: "error",
          });
        }

        this.editingTaxa[this.editingTaxa.indexOf(taxon)] = content;
      }

      for (let taxon of toDelete) {
        let { ok } = await ManagePhotoTaxonService.delete(
          this.photo.md5,
          taxon.catalogId,
        );

        if (!ok) {
          store.addNotification({
            message: "An error occurred when deleting a taxon link.",
            status: "error",
          });
        }

        this.editingTaxa.splice(this.editingTaxa.indexOf(taxon), 1);
      }

      store.addNotification({
        message: "Successfully updated taxon links.",
        status: "success",
      });
    },
  },

  watch: {
    searchText(newSearchText) {
      let currentSpecies = this.editingTaxa.map((t) => t.catalogId);
      let species = this.allSpecies.filter(
        (s) => !currentSpecies.includes(s.catalogId),
      );

      if (!newSearchText) {
        this.searchResults = species;
      }

      this.searchResults = species.filter((t) => {
        let name = t.name.toLowerCase();
        let commonName = t.commonName.toLowerCase();
        let searchText = newSearchText.toLowerCase();

        return (
          name.search(searchText) !== -1 || commonName.search(searchText) !== -1
        );
      });
    },
  },
};
</script>

<style lang="scss">
.search-results-header {
  font-weight: 700;
}

.search-results {
  ul {
    list-style-type: none;

    margin: 0;
    padding: 0;
  }

  li {
    background-color: white;

    padding: 8px;
  }
}

.search-result {
  cursor: pointer;

  &:nth-child(even) {
    background-color: rgb(245, 245, 245);
  }

  &:hover {
    background-color: rgb(220, 220, 220);
  }
}

.row-create {
  background-color: lightgreen !important;
}
.row-update {
  background-color: lightgoldenrodyellow !important;
}
.row-delete {
  background-color: lightcoral !important;
}
</style>
