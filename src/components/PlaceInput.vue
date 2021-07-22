<template>
<div>
<input :id="id_name" type="text">
</div>
</template>

<script>
export default {
name: "PlaceInput",
  props:['id_name','google'],

  data(){
  return{
    autocomplete:null,
    element:null,
  }
  },

  methods:{
  initAuto:function (){
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

  watch:{
  google(){
    this.initAuto()
  }
  }
}
</script>

<style scoped>

</style>