<template>
  <div class="stop2stop-main">
    <h2>Stop-to-stop Journey</h2>
    <div
      class=" justify-content-space-between"
    >
      <RouteSelection v-on:selectRoute="getRoute"></RouteSelection>
    </div>
    <div class="col-md-12">
      <div class="start-stop form-group">
        <StopSelection
            v-on:stopSelected="getDepStop"
            :routeinfo="routeinfo"
            placeholder="Start stop"
        ></StopSelection>
      </div>
      <div class="end-stop form-group">
        <StopSelection
            v-on:stopSelected="getArrStop"
            :routeinfo="routeinfo"
            placeholder="End stop"
        ></StopSelection>
      </div>
    </div>
    <div class="col-xs-6 col-md-8 datetime">
      <DateTimeInput
          v-on:sendTimestamp="updateTimestamp"
          gap="1em"
      ></DateTimeInput>
    </div>
    <TripRenderer
        ref="renderer"
    ></TripRenderer>
    <div class="col-12">
    <button
      @click="handle"
      type="button"
      class="submit btn btn-warning"
    >
      Submit
    </button>
      </div>
    <div v-show="show_prediction">
    <div class="col-12">
      <Prediction
          ref="predict"
          :mode="mode"
      ></Prediction>
    </div>
    </div>
  </div>
</template>

<script>
import DateTimeInput from "./DateTimeInput.vue";
import RouteSelection from "@/components/RouteSelection";
import StopSelection from "@/components/StopSelection";
import TripRenderer from "@/components/map-renderers/TripRenderer";
import Prediction from "@/components/Prediction";
export default {
  components: {
    Prediction,
    TripRenderer,
    DateTimeInput,
    RouteSelection,
    StopSelection
  },

  props:['mode'],

  data(){
    return{
      valid:false,
      route:null,
      stop_dep:null,
      stop_arr:null,
      origin: null,
      destination: null,
      direction: null,
      routeinfo: null,
      timestamp: null,
      show_prediction: false,
    }
  },

  methods:{
    getRoutes:async function(){
      let url = `/coordinate/${this.direction}/${this.route}/${this.stop_dep}/${this.stop_arr}`;
      let response = await fetch(url);
      let data = await response.json();

      if(data['valid']==2){
        alert("Origin and destination can't be the same");
        this.valid = false;
        return false;
      }
      if (data["valid"] == 1) {
        alert("The selected route is not in the same direction");
        this.valid = false;
        return false;
      }
      this.show_prediction = true;
      this.valid=true;
      this.origin = {lat: data['stop_dep']['lat'],lng:data['stop_dep']['lon']}
      this.destination = {lat: data['stop_arr']['lat'],lng:data['stop_dep']['lon']}
      await this.$refs.predict.getTripPrediction(this.route,this.direction,this.stop_dep,this.stop_arr,this.timestamp);
      return true;
    },

    handle: async function () {
      if (this.stop_arr == null || this.stop_dep == null) {
        alert("Please fill in the complete route");
        return;
      }

      if(await this.getRoutes()){
        this.$refs.renderer.displaySegment(this.route,this.stop_dep,this.stop_arr,this.direction);
      }
      else{
        this.show_prediction = false;
        this.$refs.renderer.clearView();
      }
    },

    getRoute: function (){
      this.route=arguments[0];
      this.direction=arguments[1];
      this.routeinfo=arguments;
    },

    getDepStop: function (val){
      this.stop_dep=val;
    },

    getArrStop: function (val){
      this.stop_arr=val;
    },

    updateTimestamp: function (val){
      this.timestamp = val;
    },

    refreshView: function (){
      this.$refs.renderer.clearView();
      this.$refs.predict.refreshView();
      this.show_prediction=false;
    }
  }
};
</script>

<style>

.stop2stop-main > div {
  margin-top: 2em;
}

.start-stop {
  margin-bottom: 1em;
}

.datetime {
  margin: auto; 
}

</style>