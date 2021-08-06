<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-1">
        <button class="btn menu" type="button" data-bs-toggle="collapse" data-bs-target="#input" aria-expanded="false" aria-controls="input">
          <div class="bar"></div>
          <div class="bar"></div>
          <div class="bar"></div>
        </button>
      </div>
      <div class="col-md-2">
        <img src="./assets/team.png">
      </div>
      <!-- <div class="col-sm-6 col-md-10 d-flex justify-content-end" style="margin-top: 40px; margin-bottom: 40px; z-index: 1;">
        <button type="button" class="btn btn-light">Light</button>
        <button type="button" class="btn btn-dark">Dark</button>
      </div> -->
         <Weather></Weather>
    </div>
    <div class="row">
      
      <div id="input" class="collapse col-xs-4 col-sm-5 col-md-5 col-lg-3">
        <TripSelection></TripSelection>
        <Prediction></Prediction>
      </div>
      <div class="col-md-12">
        <Map></Map>
      </div>
    </div>
    
  </div>
</template>

<style lang="scss">
@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";

#input {
  position: absolute;
  margin-top: 100px;
  margin-left: 40px;
  z-index: 2;
  background-color: #6e99f5;
  color: #F1ECED;
  border-radius: 8px;
}


.container-fluid {
  background-color: #0f567d;
  text-align: center;
  height: 100%;
}

.menu {
  position: absolute;
  display: inline-block;
  cursor: pointer;

}

.bar {
  width: 35px;
  height: 5px;
  background-color: black;
  margin: 6px 0;
}

/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 8px;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 8px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

@media only screen and (max-width: 992px) {

  #input {
    margin-top: 160px;
    margin-left: 20px;
  }
 }

@media only screen and (max-width: 600px) {

  .container-fluid {
    max-width: none;
  }
  
  #input {
    margin-top: 610px;
    margin-left: 0px;
  }

 }

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

