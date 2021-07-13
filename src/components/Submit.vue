<template>
    <div class="col-sm-2 col-md-2">
        <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
      </div>
</template>

<script>
import bus from "@/components/bus";

export default {
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

<style>

</style>