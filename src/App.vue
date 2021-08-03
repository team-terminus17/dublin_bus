<template>
  <div class="container" style="text-align: center; margin-top: 60px">
    <div class="row">
      <Weather></Weather>
      <div class="col-sm-12 col-md-12 d-flex justify-content-end">
        <button type="button" class="btn btn-light">Light</button>
        <button type="button" class="btn btn-dark">Dark</button>
      </div>
    </div>
    <Map></Map>
    <div>
      <date-time-input
          v-on:sendTimestamp="updateTimestamp"
      ></date-time-input>
    </div>
    <point-to-point-journey
        v-on:googleQueryComplete="showGooglePrediction"
        :timestamp="timestamp"
    ></point-to-point-journey>
    <stop-renderer route-filter="46A" @stop-clicked="showStopTrips"></stop-renderer>
    <bus-renderer route="46A" direction="0" inline></bus-renderer>
    <div class="row" style="margin-top: 20px;">
      <TripSelection
          v-on:tripComplete="showTripPrediction"
      ></TripSelection>
      <Prediction
          ref="predict"
      ></Prediction>
    </div>
    <stop-trips :stop-id="selectedStop"></stop-trips>
  </div>
</template>

<style lang="scss">
@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";

/*
  A basic little spinning circle from W3C:
  https://www.w3schools.com/howto/howto_css_loader.asp
*/

.loader-template {
  border: 0.7em solid #f3f3f3; /* Light grey */
  border-top: 0.7em solid #3498db; /* Blue */
  border-radius: 50%;
  width: 5em;
  height: 5em;
  animation: loader-template-spin 2s linear infinite;
}

@keyframes loader-template-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>

<script>
/* eslint-disable no-undef */
import Map from "./components/Map";
import TripSelection from "./components/TripSelection"
import Weather from "./components/Weather"
import Prediction from "./components/Prediction"
import PointToPointJourney from "@/components/PointToPointJourney";
import DateTimeInput from "@/components/DateTimeInput";
import StopRenderer from "@/components/map-renderers/StopRenderer.vue";
import BusRenderer from './components/map-renderers/BusRenderer.vue';
import StopTrips from "@/components/StopTrips.vue"

export default {
  name: "App",

  components: {
    PointToPointJourney,
    DateTimeInput,
    Map,
    TripSelection,
    Weather,
    Prediction,
    StopRenderer,
    BusRenderer,
    StopTrips
  },

  data() {
    return {
      journeyInfo: '<b>Journey Info</b>',
      timestamp: null,
      selectedStop: null,
    };
  },

  methods:{
    showTripPrediction:function (route, direction, stop_dep, stop_arr){
      this.$refs.predict.getTripPrediction(route, direction, stop_dep, stop_arr,this.timestamp);
    },

    showGooglePrediction:function (route){
      this.$refs.predict.getGooglePrediction(route, this.timestamp);
    },

    updateTimestamp:function (val){
      this.timestamp=val;
    },

    showStopTrips(stopID) {
      this.selectedStop = stopID;
    }
  }
}
</script>

