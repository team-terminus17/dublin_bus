<template>
<div>
<input :id="id_name" type="text">
</div>
</template>

<script>
export default {
name: "PlaceInput",
  props:['id_name'],

  data(){
  return{
    autocomplete:null,
    element:null,
  }
  },

  methods:{
  initAuto:function (){
    let bounds=new window.google.maps.LatLngBounds(
        {lat:52.999804, lng:-6.841221},
        {lat:53.693350, lng:-5.914248}
    );

    this.autocomplete=new window.google.maps.places.Autocomplete(
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

  computed: {
    map() {
      return this.$store.state.map;
    },
  },

  watch:{
  map(){
    this.initAuto()
  }
  }
}
</script>

<style scoped>

</style>