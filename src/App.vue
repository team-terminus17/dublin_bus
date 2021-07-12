<template>
  <div class="container" style="text-align: center; margin-top: 60px;">
      <div class="row">
         <Weather></Weather>
      <div class="col-sm-12 col-md-12 d-flex justify-content-end">
        <button type="button" class="btn btn-light">Light</button>
        <button type="button" class="btn btn-dark">Dark</button>
      </div>
    </div>
    <Map></Map>
    <TripSelection></TripSelection>
    <div class="row" style="margin-top: 20px;">
      <Prediction></Prediction>
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
export default {
  name: 'App',
  components: {
    Map,
    TripSelection,
    Weather,
    Prediction
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
