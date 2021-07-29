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
    <stop-renderer route-filter="46A"></stop-renderer>
    <bus-renderer route="46A"></bus-renderer>
    <div class="row" style="margin-top: 20px;">
      <TripSelection
          v-on:tripComplete="showTripPrediction"
      ></TripSelection>
      <Prediction
          ref="predict"
      ></Prediction>
    </div>
  </div>
</template>

<style lang="scss">
@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";
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
    BusRenderer
  },

  data() {
    return {
      journeyInfo: '<b>Journey Info</b>',
      timestamp:null,
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
    }
  }
}
</script>

