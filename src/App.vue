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
    <div class="row" style="margin-top: 20px;">
      <TripSelection></TripSelection>
      <!-- <RouteSelection
            v-on:selectRoute="getRoute"
      ></RouteSelection>
      <StopSelection
              v-on:stopSelected="getDepStop"
      ></StopSelection>
      <StopSelection
                v-on:stopSelected="getArrStop"
      ></StopSelection>
      <Submit></Submit> -->
      <Prediction></Prediction>
    </div>
  </div>
</template>

<style lang="scss">
@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";

.v-autocomplete .v-autocomplete-input-group .v-autocomplete-input {
    position: relative;
    font-size: 1.0em;
    padding: 5px 15px;
    box-shadow: none;
    border: 1px solid #157977;
    width: 100%;
    outline: none;
    background-color: #eee;
  }

.v-autocomplete .v-autocomplete-list{
    z-index: 10000;
    width: 100%;
    height: 200px;
    overflow-y:auto;
    text-align: left;
    border: none;
    border-top: none;
    max-height: 400px;
    overflow-y: auto;
    border-bottom: 1px solid #157977;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item{
      cursor: pointer;
      background-color: #fff;
      padding: 10px;
      border-bottom: 1px solid #157977;
      border-left: 1px solid #157977;
      border-right: 1px solid #157977;
      text-align: center;
}
</style>

<script>
/* eslint-disable no-undef */
import Map from "./components/Map";
import TripSelection from "./components/TripSelection"
import Weather from "./components/Weather"
import Prediction from "./components/Prediction"
// import RouteSelection from "@/components/RouteSelection";
// import StopSelection from "@/components/StopSelection";
// import Submit from './components/Submit.vue';
export default {
  name: 'App',
  components: {
    Map,
    TripSelection,
    // RouteSelection,
    // StopSelection,
    Weather,
    Prediction,
    // Submit,
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

