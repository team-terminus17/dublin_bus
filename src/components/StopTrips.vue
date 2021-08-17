<template>
  <div class="stop-trips">
    <div class="content">
      <p v-if="initial">Click on a stop to show trips</p>
      <div v-else-if="loading" class="loader-template"></div>
      <!--
        It seems on one hand that putting overflow:auto and display:flex on the
        same element leads to trouble, but on the other, putting overflow:auto
        directly on a table also leads to trouble.

        Hence the intermediate wrapper div below.
      -->
      <div class="table-wrapper" v-else-if="trips.length > 0">
        <ol>
          <li
            v-for="(trip, index) in trips"
            :key="index"
            @click="handle(trip)"
            :class="{ selected: trip.tripID === selectedTrip }"
          >
            <span>{{ trip.arrivalTime }}</span>
            <span>{{ trip.routeName }}</span>
            <!-- 
              The headsign is how one differentiates between different 
              route variants as a user, so it's important. I doesn't really fit
              at the moment, though. 
              <td>{{ trip.tripHeadsign }}</td>
            -->
          </li>
        </ol>
      </div>
      <p v-else>No trips to display</p>
    </div>
    <div class="footer">
      <button @click="track" :disabled="!selectedTrip" class="btn btn-warning">
        Track
      </button>
    </div>
  </div>
</template>

<style scoped>
.stop-trips {
  color: black;
}

.content {
  border-radius: 0.5em;
}

p {
  color: #444444;
  text-align: center;
}

.footer {
  display: inline-block;
  padding: 1em;
}

.content {
  height: 10em;
  display: flex;
  align-items: center;
  align-content: stretch;
  justify-content: center;
  background: #eee;
}

.table-wrapper {
  overflow: auto;
  height: 10em;
  padding: 1em 0.3em;
  flex-grow: 1;
}

ol {
  padding: 0;
}

li {
  display: flex;
  justify-content: space-around;
  align-content: stretch;
}

span {
  padding: 0.3em 1em;
  margin: 0.2em;
  width: 8em;
}

li.selected {
  background: var(--border-color);
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
      this.initial = false;
      this.refresh();
    },
  },
  data() {
    return {
      trips: [],
      initial: true,
      loading: false,
      selectedTrip: null,
      selectedSequence:null,
      timerID : null,
    };
  },
  created() {
    this.refresh();
  },
  methods: {
    handle(trip){
      this.selectedTrip = trip.tripID;
      this.selectedSequence=trip.sequence;
    },
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

      if (this.trips.length > 0) this.selectedTrip = this.trips[0].tripID;

      this.loading = false;
    },

    track() {
      if (!this.selectedTrip){
        alert("Please select a trip to track")
        return;
      }
      this.cancelTracking();
      this.timerID = window.setInterval(this.trackTrip,30*1000);
      this.trackTrip();
    },

    async trackTrip(){
      let time=this.fetchWaitingTime();
      if(time < 3){
        const title = 'Reminder';
            const options = {
            body: 'The selected bus is coming. Please get ready.'
          };
            navigator.serviceWorker.ready.then(function (registration){
                registration.showNotification(title,options);
            });

            this.cancelTracking();
      }
    },

    async fetchWaitingTime(){
      let url = `/time/${this.selectedTrip}/${this.stopId}/${this.selectedSequence}/trip`;
      let response = await fetch(url);
      let data = await response.json();
      return data;
    },

    cancelTracking(){
      if (this.timerID) window.clearInterval(this.timerID);
    }
  },
};
</script>
