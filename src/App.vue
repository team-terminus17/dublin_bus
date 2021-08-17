<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-sm-6 col-md-6 d-flex
        justify-content-start">
        <img src="./assets/team.png">
      </div>
      <div
      class="
        col-xs-6
        col-sm-6
        col-lg-6
        d-flex
        justify-content-end
        
      "
      id="weather"
    >
         <Weather></Weather>
      </div>
    </div>
    <div class="row">
      <div id="menu" class="col-md-1 d-flex justify-content-start">
        <button v-on:click="isShow = !isShow" class="btn btn-warning" style="cursor: pointer;">
          >
        </button>
      </div>
      <div v-show="isShow" id="input" class="col-xs-4 col-sm-5 col-md-5 col-lg-3">
        <TripSelection
            v-on:googleQueryComplete="showGooglePrediction"
            v-on:tripComplete="showTripPrediction"
            v-on:tabChanged="refreshView"
        ></TripSelection>
        <Prediction
            ref="predict"
        ></Prediction>
      </div>
      <div class="col-md-12">
        <Map></Map>
      </div>
    </div>
    
  </div>
</template>

<style lang="scss">
@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";

:root {
  --background-color: #e2e2e2;
  --border-color: #e59c24;
  --border-radius: 8px;

}

#input {
  position: absolute;
  margin-top: 90px;
  margin-left: 40px;
  z-index: 2;
  background-color: #0f567d;
  color: #F1ECED;
  border-radius: var(--border-radius);
}

#weather {
  z-index: 1;
}


.container-fluid {
  background-color: #0f567d;
  text-align: center;
  height: 100%;
}

#menu {
  position: absolute;
  display: inline-block;
  z-index: 1;
  margin-top: 100px;
  
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
  border-radius: var(--border-radius);
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: var(--border-radius);
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

@media only screen and (max-width: 992px) {

  #input {
    margin-left: 40px;
  }

  #weather {
    margin-left: 0%; 
  }

 }

@media only screen and (max-width: 600px) {

  .container-fluid {
    max-width: none;
    max-height: none;
  }
  
  #input {
    margin-top: 550px;
    margin-left: 0px;
    border-radius: 0px;
  }

  #weather {
    position: absolute;
  }

  img {
    width: 50%;
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

export default {
  name: "App",

  components: {
    Map,
    TripSelection,
    Weather,
    Prediction,
  },

  data() {
    return {
      journeyInfo: '<b>Journey Info</b>',
      timestamp: null,
      selectedStop: null,
      isShow: true,
    };
  },

  methods:{
    showTripPrediction:function (route, direction, stop_dep, stop_arr, timestamp){
      this.$refs.predict.getTripPrediction(route, direction, stop_dep, stop_arr, timestamp);
    },

    showGooglePrediction:function (route, timestamp){
      this.$refs.predict.getGooglePrediction(route, timestamp);
    },

    updateTimestamp:function (val){
      this.timestamp=val;
    },

    showStopTrips(stopID) {
      this.selectedStop = stopID;
    },

    refreshView(){
      this.$refs.predict.refreshView();
    }
  }
}
</script>

