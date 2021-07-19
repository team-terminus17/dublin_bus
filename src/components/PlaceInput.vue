<template>
<div>
<input :id="id_name" type="text">
</div>
</template>

<script>
import bus from "@/components/bus";
export default {
name: "PlaceInput",
  props:{
  id_name:{
    type:String
  }
  },

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
    let bounds=new this.google.maps.LatLngBounds(
        {lat:52.999804, lng:-6.841221},
        {lat:53.693350, lng:-5.914248}
    );

    this.autocomplete=new this.google.maps.places.Autocomplete(
        document.getElementById(this.id_name),
        {
          bounds:bounds,
          fields:['place_id','geometry','name'],
          strictBounds:true
        });
    this.autocomplete.addListener('place_changed',this.onPlaceChanged);
  },

    onPlaceChanged:function (){
    let place=this.autocomplete.getPlace();
    this.$emit("sendPlaceID",place.place_id)
    }
  },

  created() {
  bus.$on("sendGoogle",this.initAuto);
  },
}
</script>

<style scoped>

</style>