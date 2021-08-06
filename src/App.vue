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

</style>

<script>
/* eslint-disable no-undef */
import Map from "./components/Map";
import TripSelection from "./components/TripSelection"
import Weather from "./components/Weather"
import Prediction from "./components/Prediction"
import PointToPointJourney from "@/components/PointToPointJourney";
export default {
  name: 'App',
  components: {
    Map,
    TripSelection,
    Weather,
    Prediction,
  },
  data() {
    return {
      greet: 'Hello there',
      name: "General Kenobi",
      headingID: 'heading',
      isDisabled: false,
      status: 'success',
      journeyInfo: '<b>Journey Info</b>',

      predict:{
        time: "test",
      },

    };
  },
}
</script>

