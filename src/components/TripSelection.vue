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
          ></StopSelection>
        </div>
        <div class="form-group" style="margin-top: 20px;">
          <label class="d-flex justify-content-start">Destination Stop</label>
          <StopSelection
              v-on:stopSelected="getArrStop"
          ></StopSelection>
        </div>
    </div>
    <div class="col-sm-2 col-md-4" style="margin-top: 20px;">
      <div style="margin-top: 20px;">
      <DateInput v-model="date"></DateInput>
      </div>
      <div style="margin-top: 20px;">
      <TimeInput v-model="time"></TimeInput>
      </div>
    </div>
    <div class="col-sm-2 col-md-2">
      <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
    </div>
    </div>
  </div>
</template>

<script>

import Vue from "vue"
import Component from "vue-class-component"
import bus from "@/components/bus";
import RouteSelection from "@/components/RouteSelection";
import StopSelection from "@/components/StopSelection";
import DateInput from "@/components/DateInput";
import TimeInput from "@/components/TimeInput";

// @Component
// export default class TripSelection extends Vue {
//   journey = "Please input your journey info:"
// }
export default {
  name: "TripSelection",
  components:{
    RouteSelection,
    StopSelection,
    DateInput,
    TimeInput,
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
      time: "3:00",
      date: null, 
    }
  },
  methods:{
    getRoutes:async function(){
      let url = '/coordinate/'+'/'+this.route+'/'+this.stop_dep+'/'+this.stop_arr;
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
      bus.$emit("showDirection",this.origin,this.destination);
  },
    handle() {
      if (this.stop_arr == null || this.stop_dep == null) {
        alert("Please fill in the complete route");
        return;
      }
      this.getRoutes();
  },
    getRoute: function (val){
      this.route=val;
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

</style>