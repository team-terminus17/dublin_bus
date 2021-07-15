<template>
<div>
<input id="autocomplete" type="text">
</div>
</template>

<script>
import bus from "@/components/bus";
export default {
name: "PlaceInput",
  data(){
  return{
    autocomplete:null,
    element:null,
    google:null
  }
  },
  methods:{
  initAuto:function (val){
    this.google=val;
    if(this.google){
      let bounds=new this.google.maps.LatLngBounds(
        {lat:52.999804, lng:-6.841221},
        {lat:53.693350, lng:-5.914248}
    );
    this.autocomplete=new this.google.maps.places.Autocomplete(
        document.getElementById('autocomplete'),
        {
          bounds:bounds,
          fields:['place_id','geometry','name'],
          strictBounds:true
        });
    }

  }
  },
  created() {
  bus.$on("sendGoogle",this.initAuto);
  },
}
</script>

<style scoped>

</style>