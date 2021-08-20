<template>
  <div style="position: relative">
    <div id="realtime_header">
    <h2>Real Time
      <img src="https://img.icons8.com/small/16/ffffff/info.png" id="info_img">
    </h2>
    <div v-html="instruction_info" id="track_instruction"></div>
    </div>
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
        :stop="stop"
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

#realtime_header:hover #track_instruction{
  visibility: visible;
}

#track_instruction{
  font-size: small;
  font-weight: normal;
  visibility: hidden;
  /*margin: 20px;*/

  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  position: absolute;
  z-index: 1;
}

#info_img{
  width: 20px;
  height: 20px;
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
      instruction_info:'<h5>Instructions on tracking</h5>' +
          '<p>First choose a trip to track, and when you click track button,' +
          'the app will push a notification when the bus is coming in three minutes</p>' +
          '<p> Press the button again to stop tracking.</p>'
    };
  },
  methods: {
    onRouteSelected(route, direction) {
      this.route = route;
      this.direction = direction.toString();
    },
    onStopClicked(stop) {
      this.stop = stop;
      this.$refs.stoptrips.cancelTracking();
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