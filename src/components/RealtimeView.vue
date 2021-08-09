<template>
  <div>
    <div class="route-selection">
      <RouteSelection @selectRoute="onRouteSelected"></RouteSelection>
    </div>
    <StopRenderer
      :showMarkers="route != null"
      :routeFilter="route"
      :directionFilter="direction"
      @stop-clicked="onStopClicked"
    ></StopRenderer>
    <BusRenderer :route="route" :direction="direction"></BusRenderer>
    <StopTrips :stopId="stop"></StopTrips>
  </div>
</template>

<style scoped>

.route-selection {
  margin-bottom: 1em;
}

.stop-trips {
  margin-bottom: 1em;
}

</style>

<script>
import RouteSelection from "./RouteSelection.vue";
import StopRenderer from "./map-renderers/StopRenderer.vue";
import BusRenderer from "./map-renderers/BusRenderer.vue";
import StopTrips from "./StopTrips.vue";

export default {
  name: "RealtimeView",
  components: {
    RouteSelection,
    StopRenderer,
    BusRenderer,
    StopTrips,
  },
  data() {
    return {
      route: null,
      direction: null,
      stop: null,
    };
  },
  methods: {
    onRouteSelected(route, direction) {
      this.route = route;
      this.direction = direction.toString();
    },
    onStopClicked(stopID) {
      this.stop = stopID;
    },
  },
};
</script>