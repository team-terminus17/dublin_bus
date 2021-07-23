<template>
  <!--
      This component renders to the map and doesn't
      need any html elements. Is there a better element 
      to use here / a better way of declaring a component
      that does not render directly?
  -->
  <div></div>
</template>

<script>
export default {
  name: "StopRenderer",

  props: {
    showMarkers: {
      type: Boolean,
      default: true,
    },

    agencyFilter: {
      type: String,
      default: "all",
    },

    routeFilter: {
      type: String,
      default: "all",
    },

    directionFilter: {
      type: String,
      default: "both",
    },

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
    map: "refreshView"
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
      return this.$store.state.map
    }
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

      // Is there a way of clearing an array in javascript
      // that is considered more 'proper'?
      this.markers.splice(0, this.markers.length);
    },

    refreshMarkers() {
      this.removeMarkers();

      if (!this.map) return;
      if (!this.showMarkers) return;

      for (const stop of Object.values(this.stopsData)) {
        if (this.isVisible(stop)) {
          const marker = new window.google.maps.Marker({
            position: {
              lat: stop.lat,
              lng: stop.lng,
            },
            map: this.map,
          });
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
