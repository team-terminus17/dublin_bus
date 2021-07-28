<template>
  <div class="col-sm-12 col-md-9">
    <div v-html="journey" class="d-flex"></div>
    <div class="row">
    <div class="col-md-2 justify-content-space-between" style="margin-top: 30px;">
      <label class="d-flex justify-content-start">Route Selection</label>
        <RouteSelection
            v-on:selectRoute="getRoute"
        ></RouteSelection>
    </div>
    <div class="col-md-4">
        <div class="form-group" style="margin-top: 6px;">
          <label class="d-flex justify-content-start">Origin Stop</label>
          <StopSelection
              v-on:stopSelected="getDepStop"
              :routeinfo="routeinfo"
          ></StopSelection>
        </div>
        <div class="form-group" style="margin-top: 20px;">
          <label class="d-flex justify-content-start">Destination Stop</label>
          <StopSelection
              v-on:stopSelected="getArrStop"
              :routeinfo="routeinfo"
          ></StopSelection>
        </div>
    </div>
      <trip-renderer
          ref="renderer"
      ></trip-renderer>
    <div class="col-sm-2 col-md-2">
      <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
    </div>
    </div>
  </div>
</template>

<script>

import RouteSelection from "@/components/RouteSelection";
import StopSelection from "@/components/StopSelection";
import TripRenderer from "@/components/map-renderers/TripRenderer";

export default {
  name: "TripSelection",
  components:{
    TripRenderer,
    RouteSelection,
    StopSelection,
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
      routeinfo: null
    }
  },
  methods:{
    getRoutes:async function(){
      let url = `/coordinate/${this.direction}/${this.route}/${this.stop_dep}/${this.stop_arr}`;
      let response = await fetch(url);
      let data = await response.json();

      if(data['valid']==2){
        alert("Origin and destination can't be the same");
        this.valid=false;
        return ;
      }
      if (data['valid']==1){
        alert("The selected route is not in the same direction");
        this.valid=false;
        return ;
      }
      this.valid=true;
      this.origin = {lat: data['stop_dep']['lat'],lng:data['stop_dep']['lon']}
      this.destination = {lat: data['stop_arr']['lat'],lng:data['stop_dep']['lon']}
      this.$emit("tripComplete",this.route,this.direction,this.stop_dep,this.stop_arr)
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
  }
  },

}
</script>

<style scoped>

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