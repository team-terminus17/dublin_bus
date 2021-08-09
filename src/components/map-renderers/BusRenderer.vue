<template>
  <div></div>
</template>

<style>
/* Do not scope this! This is for google. */
.gm-style-iw button {
  display: none !important;
}
.gm-style-iw {
  text-align: center;
}
</style>

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
      default: null,
    },
    /**
     * Filter by direction - '0' for outbound, '1' for inbound.
     * @values 0,1,both
     */
    direction: {
      type: String,
      default: "both",
    },
    /**
     * If true, show the icons in line with the stops
     * as opposed to in an info window. Defaults to false.
     */
    inline: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    route: "refreshView",
    direction: "refreshView",
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
    this.timerID = window.setInterval(
      () => this.refreshView(false),
      15 * 1000 // seconds
    );
  },
  beforeDestroy() {
    this.clearView();
    if (this.timerID) window.clearInterval(this.timerID);
  },
  methods: {
    refreshView(transition = true) {
      if (this.loading) return;
      this.loading = true;
      if (transition) this.clearView();

      this.fetchData().then(() => {
        if (!transition) this.clearView();
        this.drawIcons();
        this.loading = false;
      });
    },
    async fetchData() {
      if (!this.route || !this.agency) {
        this.tripData = [];
        this.stopLookup = new Map();
        return;
      }
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
      for (let popup of this.popups) popup.setMap(null);
      this.popups = [];
    },
    drawIcons() {
      if (!this.map) return;
      if (!this.stopLookup) return;
      if (!this.tripData) return;

      for (const trip of this.tripData) {
        if (this.direction != "both" && this.direction != trip.direction)
          continue;

        const stop = this.stopLookup.get(trip.currentStop);
        const nextStop = this.stopLookup.get(trip.nextStop);

        const deltaX = nextStop.lng - stop.lng;
        let direction = "r";
        if (deltaX < 0) direction = "l";

        const icon = {
          url: require(`@/assets/bus-${direction}.png`),
          scaledSize: new window.google.maps.Size(30, 15),
        };

        const marker = new window.google.maps.Marker({
          position: {
            lat: stop.lat,
            lng: stop.lng,
          },
          icon: icon,
          map: this.map,
          visible: this.inline,
        });

        this.markers.push(marker);

        if (!this.inline) {
          const style = `style="width:30px;height:15px;"`;
          const popup = new window.google.maps.InfoWindow({
            content: `<img ${style} src="${require(`@/assets/bus-${direction}.png`)}" />`,
            disableAutoPan: true,
          });

          popup.open({
            anchor: marker,
            map: this.map,
            shouldFocus: false,
          });

          this.popups.push(popup);
        }
      }
    },
  },
};
</script>
