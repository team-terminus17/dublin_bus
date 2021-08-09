<template>
  <div>
    <div v-html="journey" class="d-flex"></div>
    <div
      class="col-md-4 justify-content-space-between"
      style="margin-top: 20px"
    >
      <label class="d-flex justify-content-start">Route Selection</label>
      <RouteSelection v-on:selectRoute="getRoute"></RouteSelection>
    </div>
    <div class="col-md-12">
      <div class="form-group" style="margin-top: 6px">
        <label class="d-flex justify-content-start">Start Stop</label>
        <StopSelection
            v-on:stopSelected="getDepStop"
            :routeinfo="routeinfo"
        ></StopSelection>
      </div>
      <div class="form-group" style="margin-top: 10px">
        <label class="d-flex justify-content-start">End Stop</label>
        <StopSelection
            v-on:stopSelected="getArrStop"
            :routeinfo="routeinfo"
        ></StopSelection>
      </div>
    </div>
    <div class="col-md-12" style="margin-top: 10px">
      <DateTimeInput
          v-on:sendTimestamp="updateTimestamp"
      ></DateTimeInput>
    </div>
    <TripRenderer
        ref="renderer"
    ></TripRenderer>
    <button
      @click="handle"
      type="button"
      class="btn btn-warning"
      style="margin-top: 70px"
    >
      Submit
    </button>
  </div>
</template>

<script>
import DateTimeInput from "./DateTimeInput.vue";
import RouteSelection from "@/components/RouteSelection";
import StopSelection from "@/components/StopSelection";
import TripRenderer from "@/components/map-renderers/TripRenderer";
export default {
  components: {
    TripRenderer,
    DateTimeInput,
    RouteSelection,
    StopSelection
  },

  data(){
    return{
      valid:false,
      route:null,
      stop_dep:null,
      stop_arr:null,
      journey :"Please input your journey info:",
      origin: null,
      destination: null,
      direction: null,
      routeinfo: null,
      timestamp: null
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
        return;
      }
      if (data["valid"] == 1) {
        alert("The selected route is not in the same direction");
        this.valid = false;
        return;
      }
      this.valid=true;
      this.origin = {lat: data['stop_dep']['lat'],lng:data['stop_dep']['lon']}
      this.destination = {lat: data['stop_arr']['lat'],lng:data['stop_dep']['lon']}
      this.$emit("tripComplete",this.route,this.direction,this.stop_dep,this.stop_arr,this.timestamp)
    },

    handle() {
      if (this.stop_arr == null || this.stop_dep == null) {
        alert("Please fill in the complete route");
        return;
      }
      this.getRoutes();
      this.$refs.renderer.displaySegment(this.route,this.stop_dep,this.stop_arr,this.direction);
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
    }
  }
};
</script>

<style>
</style>