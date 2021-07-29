<template>
  <div></div>
</template>

<script>
/**
 * Renders stops on the google map in the Vuex store.
 *
 * By default, renders all stops for all agencies, which takes quite some time
 * to load.
 *
 * There are properties which allow filtering by agency, route, and direction.
 */
export default {
  name: "StopRenderer",

  props: {
    showMarkers: {
      type: Boolean,
      default: true,
    },
    /**
     * Filter by agency. This should be in the form of a GTFS ID
     * e.g. '978' for Dublin Bus
     */
    agencyFilter: {
      type: String,
      default: "all",
    },
    /**
     * Filter by the short name of a route.
     * Any letters should be capitalized.
     * e.g. '46A'
     */
    routeFilter: {
      type: String,
      default: "all",
    },
    /**
     * Filter by direction - '0' for outbound, '1' for inbound.
     * @values 0,1,both
     */
    directionFilter: {
      type: String,
      default: "both",
    },
    /**
     * By default, only stops for a representative "main"
     * path a route takes are shown. Set this to true to
     * show all stops associated with the route.
     */
    showVariants: {
      type: Boolean,
      default: false,
    },
  },

  watch: {
    showMarkers: "refreshView",
    agencyFilter: "refreshView",
    routeFilter: "refreshView",
    directionFilter: "refreshView",
    map: "refreshView",
  },

  data() {
    return {
      loading: false,
      stopsData: null,
      markers: [],
    };
  },

  computed: {
    map() {
      return this.$store.state.map;
    },
  },

  created() {
    this.refreshView();
  },

  beforeDestroy() {
    this.removeMarkers();
  },

  methods: {
    refreshView() {
      if (this.loading) return;
      this.loading = true;

      this.fetchData((data) => {
        this.stopsData = data;
        this.refreshMarkers();
        this.loading = false;
      });
    },

    fetchData(callback) {
      if (!this.showMarkers) callback({});
      else {
        const url = `/stops/${this.agencyFilter}/${this.routeFilter}/info`;

        fetch(url)
          .then((response) => response.json())
          .then(callback);
      }
    },

    removeMarkers() {
      for (let marker of this.markers) marker.setMap(null);
      this.markers = [];
    },

    refreshMarkers() {
      this.removeMarkers();

      if (!this.map) return;
      if (!this.showMarkers) return;

      const icon = {
        url: require("@/assets/circle-10.png"),
        scaledSize: new window.google.maps.Size(10,10)
      }

      for (const stop of this.stopsData) {
        if (this.isVisible(stop)) {
          const marker = new window.google.maps.Marker({
            position: {
              lat: stop.lat,
              lng: stop.lng,
            },
            icon: icon,
            map: this.map
          });
          this.markers.push(marker);
        }
      }
    },

    isVisible(stop) {
      for (const route of stop.routes) {
        if (
          (this.agencyFilter == "all" || route.agency == this.agencyFilter) &&
          (this.routeFilter == "all" || route.name == this.routeFilter) &&
          (this.directionFilter == "both" ||
            route.direction == this.directionFilter) &&
          (this.showVariants || route.main)
        )
          return true;
      }

      return false;
    },
  },
};
</script>
