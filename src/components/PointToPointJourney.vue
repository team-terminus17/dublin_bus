<template>
<div>
  <PlaceInput
      id_name="autocomplete1"
      v-on:sendPlaceID="getStart"
  ></PlaceInput>
<!--  id_name is set to differentiate between two placeinput components-->
  <PlaceInput
      id_name="autocomplete2"
      v-on:sendPlaceID="getEnd"
  ></PlaceInput>
  <PointToPointRenderer
      v-on:directionsValidated="showGooglePrediction"
      ref="renderer"
  ></PointToPointRenderer>
  <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
</div>
</template>

<script>
import PlaceInput from "@/components/PlaceInput";
import PointToPointRenderer from "@/components/map-renderers/PointToPointRenderer";
export default {
  name: "PointToPointJourney",

  components: {
    PointToPointRenderer,
    PlaceInput
  },

  props:['timestamp'],

  data(){
    return{
      start:null,
      end:null
    }
  },

  methods: {
    handle: function () {
      if(this.start==null||this.end==null){
        alert("You need to enter both origin and destination.");
      }
      else{
        this.renderRoute();
      }
    },

    getStart: function (val){
      this.start=val;
    },

    getEnd: function (val){
      this.end=val;
    },

    renderRoute:function (){
      this.$refs.renderer.getGoogleTime(this.start,this.end,this.timestamp);
    },

    showGooglePrediction: function (route){
      this.$emit("googleQueryComplete",route);
    }
  }
}
</script>

<style scoped>

</style>