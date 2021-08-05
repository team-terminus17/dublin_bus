<template>
  <div class="stop-trips">
    <div v-if="loading" class="loader-template"></div>
    <!--
      It seems on one hand that putting overflow:auto and display:flex on the
      same element leads to trouble, but on the other, putting overflow:auto
      directly on a table also leads to trouble.

      Hence the intermediate wrapper div below.
    -->
    <div class="table-wrapper" v-else-if="trips.length > 0">
      <table>
        <tr v-for="(trip, index) in trips" :key="index">
          <td>{{trip.arrivalTime}}</td><td>{{trip.tripHeadsign}}</td>
          <button @click="track(trip.tripID)">Track</button>
        </tr>
      </table>
    </div>
    <p v-else>No trips to display</p>
  </div>
</template>

<style scoped>

.stop-trips {
  height: 10em;
  width: 30em;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: #eee;
  margin: 2em;
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

button {
  padding: 0.3em;
  border: none;
  background: #d5d5d5;
  border-radius: 0.25em;
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
    }
  },
  data() {
    return {
      trips: [],
      loading: false,
    };
  },
  created() {
    this.refresh();
  },
  methods: {
    async refresh() {
      this.trips = [];
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

      this.loading = false;
    },
  },
};
</script>
