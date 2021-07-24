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
        v-on:googlequerycomplete="showGooglePrediction"
        :timestamp="timestamp"
    ></point-to-point-journey>
    <div class="row" style="margin-top: 20px;">
      <TripSelection
          v-on:tripcomplete="showTripPrediction"
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
export default {
  name: "App",

  components: {
    PointToPointJourney,
    DateTimeInput,
    Map,
    TripSelection,
    Weather,
    Prediction,
  },

  data() {
    return {
      journeyInfo: '<b>Journey Info</b>',
      timestamp:null,
    };
  },

  methods:{
    showTripPrediction:function (){
      this.$refs.predict.getTripPrediction(arguments[0],arguments[1],arguments[2],arguments[3],this.timestamp)
    },

    showGooglePrediction:function (val){
      this.$refs.predict.getGooglePrediction(val, this.timestamp);
    },

    updateTimestamp:function (val){
      this.timestamp=val
    }
  }
}
</script>

