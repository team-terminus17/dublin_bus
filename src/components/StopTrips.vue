<template>
  <section class="stop-trips">
    <div class="content">
      <div v-if="loading" class="loader-template"></div>
      <!--
        It seems on one hand that putting overflow:auto and display:flex on the
        same element leads to trouble, but on the other, putting overflow:auto
        directly on a table also leads to trouble.

        Hence the intermediate wrapper div below.
      -->
      <div class="table-wrapper" v-else-if="trips.length > 0">
        <table>
          <tr
            v-for="(trip, index) in trips"
            :key="index"
            @click="selectedTrip = trip.tripID"
            :class="{selected: trip.tripID === selectedTrip}"
          >
            <td>{{ trip.arrivalTime }}</td>
            <td>{{ trip.routeName }}</td>
            <td>{{ trip.tripHeadsign }}</td>
          </tr>
        </table>
      </div>
      <p v-else>No trips to display</p>
    </div>
    <footer>
      <button @click="track" :disabled="!selectedTrip">Track</button>
    </footer>
  </section>
</template>

<style scoped>
.stop-trips {
  margin: 2em;
  display: inline-grid;
}

footer {
  display: inline;
  padding: 1em;
}

.content {
  height: 10em;
  width: 30em;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eee;
}

.table-wrapper {
  overflow: auto;
  height: 10em;
  padding: 1em 0.3em;
}

td {
  padding: 0.3em 1em;
  vertical-align: middle;
  margin: 0.2em;
}

tr.selected {
  background: #aaaaff;
}

button {
  padding: 0.3em;
  border: none;
  background: #d5d5d5;
  border-radius: 0.25em;
  transition: background 0.3s;
}

button:disabled {
  color: #aaaaaa;
}

button:hover {
  background: rgb(160, 160, 160);
}


button:active {
  background: rgb(85, 85, 85);
}

</style>

<script>
/**
 * Displays a list of trips arriving to a specific stop.
 */
export default {
  name: "StopTrips.vue",
  /**
   * The stop to display trips for.
   *
   * This should be an internal stop ID, such as that as returned by the
   * /stop/<agency>/<route>/info endpoint and used by the stop renderer.
   */
  props: ["stopId"],
  watch: {
    stopId() {
      this.refresh();
    },
  },
  data() {
    return {
      trips: [],
      loading: false,
      selectedTrip: null,
    };
  },
  created() {
    this.refresh();
  },
  methods: {
    clear() {
      this.trips = [];
      this.selectedTrip = null;
    },
    async refresh() {
      this.clear();
      if (!this.stopId) return;
      this.loading = true;

      const response = await fetch(`stops/${this.stopId}/trips`);

      if (response.ok) {
        const data = await response.json();
        this.trips = data;
      } else {
        console.error(
          `Failed to retrieve data for stop with ID '${this.stopId}'`
        );
      }

      if (this.trips.length > 0)
        this.selectedTrip = this.trips[0].tripID;

      this.loading = false;
    },
    track() {
      if (this.selectedTrip) this.$emit("track", this.selectedTrip);
    },
  },
};
</script>
