<template>
  <div>
    <div class="row">
        <div v-html="journey" class="d-flex justify-content-start"></div>
    </div>
     <div class="col-sm-3 col-md-2" style="margin-top: 30px;">
<!--        <div class="btn-group">-->
<!--          <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">-->
<!--            Bus Route-->
<!--          </button>-->
<!--          <ul class="dropdown-menu">-->
<!--            <li><a class="dropdown-item" href="#">9</a></li>-->
<!--            <li><a class="dropdown-item" href="#">46a</a></li>-->
<!--            <li><a class="dropdown-item" href="#">145</a></li>-->
<!--            <li><hr class="dropdown-divider"></li>-->
<!--            <li><a class="dropdown-item" href="#">Separated link</a></li>-->
<!--          </ul>-->
<!--        </div>-->
        <RouteSelection
            v-on:selectRoute="getRoute"
        ></RouteSelection>
      </div>
      <div class="col-sm-3 col-md-2">
        <form>
          <div class="form-group" style="margin-top: 6px;">
            <label class="d-flex justify-content-start">Origin Stop</label>
<!--            <input type="origin" class="form-control" id="originStop" placeholder="Enter origin stop">-->
            <StopSelection
                v-on:stopSelected="getDepStop"
            ></StopSelection>
          </div>
          <div class="form-group" style="margin-top: 6px;">
            <label class="d-flex justify-content-start">Destination Stop</label>
            <StopSelection
                v-on:stopSelected="getArrStop"
            ></StopSelection>
<!--            <input type="destination" class="form-control" id="destinationStop" placeholder="Enter destination stop">-->
          </div>
        </form>
      </div>
      <div class="col-sm-4 col-md-3">
        <div class="btn-group" style="margin-top: 30px;">
          <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            Day of the Week
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Monday</a></li>
            <li><a class="dropdown-item" href="#">Tuesday</a></li>
            <li><a class="dropdown-item" href="#">Wednesday</a></li>
            <li><a class="dropdown-item" href="#">Thursday</a></li>
            <li><a class="dropdown-item" href="#">Friday</a></li>
            <li><a class="dropdown-item" href="#">Saturday</a></li>
            <li><a class="dropdown-item" href="#">Sunday</a></li>
          </ul>
        </div>
        <div class="btn-group" style="margin-top: 30px;">
          <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            Departure time
          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">9</a></li>
            <li><a class="dropdown-item" href="#">46a</a></li>
            <li><a class="dropdown-item" href="#">145</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Separated link</a></li>
          </ul>
        </div>
      </div>
      <div class="col-sm-2 col-md-2">
        <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
      </div>
  </div>
</template>

<script>

import Vue from "vue"
import Component from "vue-class-component"
import bus from "@/components/bus";
import RouteSelection from "@/components/RouteSelection";
import StopSelection from "@/components/StopSelection";

// @Component
// export default class TripSelection extends Vue {
//   journey = "Please input your journey info:"
// }
export default {
  name: "TripSelection",
  components:{
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