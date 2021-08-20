<template>
<div>
<input
    :id="id_name"
    type="text"
    :placeholder="place_holder"
    v-bind:value="address"
>
</div>
</template>

<script>
export default {
name: "PlaceInput",
  props:['id_name','place_holder',],

  data(){
  return{
    autocomplete:null,
    element:null,
    address:null
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
    this.$emit("sendPlaceID",place.place_id);
    },

    changeAddress: function (val){
      document.getElementById(this.id_name).value=val;
    }
  },

  computed: {
    map() {
      return this.$store.state.map;
    },
  },

  watch:{
  map(){
    this.initAuto();
  }
  }
}
</script>

<style scoped>

input {
  background-color: var(--background-color);
  width: 100%;
  border-color: var(--border-color);
  border-radius: var(--border-radius);
  color: var(--font-color);
  padding: 5px 15px;
  font-size: 1em;
  border-width: 1px;
}
</style>