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
  <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
</div>
</template>

<script>
import PlaceInput from "@/components/PlaceInput";
import bus from "@/components/bus";
export default {
  name: "PointToPointJourney",

  components: {
    PlaceInput
  },

  data(){
    return{
      start:null,
      end:null,
    }
  },

  methods: {
    handle: function () {
      if(this.start==null||this.end==null){
        alert("You need to enter both origin and destination.")
      }
      else{
        bus.$emit("sendLocation",this.start,this.end)//emit to map component
      }
    },

    getStart: function (val){
      this.start=val
    },

    getEnd: function (val){
      this.end=val
    }
  }
}
</script>

<style scoped>

</style>