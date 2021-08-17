<template>
  <div>
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
    </div>
    <button
      @click="handle"
      type="button"
      class="btn btn-warning"
      style="margin-top: 40px"
    >
      Submit
    </button>
  </div>
</template>

<script>

import RouteSelection from "@/components/RouteSelection.vue"
import StopSelection from "@/components/StopSelection";

export default {
  components: {
    RouteSelection,
    StopSelection,
  },

  data(){
    return {
      route:null,
      direction: null,
      routeinfo: null,
      stop_dep:null,

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

    getRoute: function (){
      this.route=arguments[0];
      this.direction=arguments[1];
      this.routeinfo=arguments;
    },

    getDepStop: function (val){
      this.stop_dep=val;
    },

    refreshView: function (){
      this.$refs.renderer.clearView();
    }
}
}


</script>

<style>

</style>