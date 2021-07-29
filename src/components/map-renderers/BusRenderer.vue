<template>
  <div></div>
</template>

<script>
/**
 * Renders buses for a specific agency/route as little popups above
 * the route.
 *
 * There is an optional direction filter.
 */
export default {
  name: "BusRenderer",
  props: {
    /**
     * Specify the agency. Showing buses for all agencies
     * at once is currently not supported.
     */
    agency: {
      type: String,
      default: "978",
    },
    /**
     * Specify the route. Showing buses for all routes at once
     * is currently not supported.
     */
    route: {
      type: String,
      default: "46A",
    },
    /**
     * Filter by direction - '0' for outbound, '1' for inbound.
     * @values 0,1,both
     */
    directionFilter: {
      type: String,
      default: "both",
    },
  },
  watch: {
    route: "refreshView",
    directionFilter: "refreshView",
    map: "refreshView",
  },
  data() {
    return {
      loading: false,
      stopLookup: null,
      tripData: null,
      markers: [],
      popups: [],
      timerID: null,
    };
  },
  computed: {
    map() {
      return this.$store.state.map;
    },
  },
  created() {
    this.refreshView();
    this.timerID = window.setInterval(() => this.refreshView(false), 15 * 1000);
  },
  beforeDestroy() {
    this.clearView();
    if (this.timerID) window.clearInterval(this.timerID);
  },
  methods: {
    refreshView(transition=true) {
      if (this.loading) return;
      this.loading = true;
      if (transition) this.clearView();

      this.fetchData().then(() => {
        if (!transition) this.clearView()
        this.drawIcons();
        this.loading = false;
      });
    },
    async fetchData() {
      const stopUrl = `/stops/${this.agency}/${this.route}/info`;
      const stops = fetch(stopUrl).then((response) => response.json());

      const tripUrl = `/trips/${this.agency}/${this.route}/current`;
      const trips = fetch(tripUrl).then((response) => response.json());

      this.stopLookup = new Map();
      const stopData = await stops;
      for (const item of stopData) this.stopLookup.set(item.ID, item);

      this.tripData = await trips;
    },
    clearView() {
      for (let marker of this.markers) marker.setMap(null);
      this.markers = [];
    },
    drawIcons() {
      if (!this.map) return;
      if (!this.stopLookup) return;
      if (!this.tripData) return;

      const icon = {
        url: require("@/assets/bus.png"),
        scaledSize: new window.google.maps.Size(30, 30),
      };

      for (const trip of this.tripData) {
        const stop = this.stopLookup.get(trip.currentStop);

        const marker = new window.google.maps.Marker({
          position: {
            lat: stop.lat,
            lng: stop.lng,
          },
          icon: icon,
          map: this.map,
        });

        this.markers.push(marker);
      }
    },
  },
};
</script>
