<template>
  <div>
    <div class="route-selection">
      <RouteSelection
          @selectRoute="onRouteSelected"
          ref="route"
      ></RouteSelection>
    </div>
    <StopRenderer
      :showMarkers="route != null"
      :routeFilter="route"
      :directionFilter="direction"
      @stop-clicked="onStopClicked"
      ref="stoprenderer"
    ></StopRenderer>
    <BusRenderer
        :route="route"
        :direction="direction"
        ref="busrenderer"
    ></BusRenderer>
    <StopTrips
        :stopId="stop"
        :sequence="sequence"
        ref="stoptrips"
    ></StopTrips>
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
      sequence: null,
    };
  },
  methods: {
    onRouteSelected(route, direction) {
      this.route = route;
      this.direction = direction.toString();
    },

    onStopClicked(stopID, sequence) {
      this.stop = stopID;
      this.sequence = sequence;
    },

    refreshView: function (){
      this.$refs.stoprenderer.removeMarkers();
      this.$refs.busrenderer.clear();
      this.$refs.stoptrips.clear();
      this.$refs.route.clearView();
    }
  },
};
</script>