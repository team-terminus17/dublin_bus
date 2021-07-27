<template>
  <div class="container-fluid" style="text-align: center; margin-top: 5px;">
    <div class="row">
      <div class="col-sm-6 col-md-10 d-flex justify-content-end" style="margin-top: 40px; margin-bottom: 40px; z-index: 1;">
        <button type="button" class="btn btn-light">Light</button>
        <button type="button" class="btn btn-dark">Dark</button>
      </div>
         <Weather></Weather>
    </div>
    <div class="row">
      <div id="input" class="col-md-2">
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
  margin-left: 40px;
  margin-top: -30px;
  margin-bottom: -10px;
  z-index: 1;
  background-color: #4a80f5;
  color: #F1ECED;
  border-radius: 8px;
}

// .container-fluid {
//   background-color: #E89D38;
// }

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

