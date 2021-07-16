<template>
<div>
  <PlaceInput
      :id_name="id1"
      v-on:sendPlaceID="getStart"
  ></PlaceInput>
  <PlaceInput
      :id_name="id2"
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
      id1:"autocomplete1",
      id2:"autocomplete2",
      start:null,
      end:null,
    }
  },
  methods: {
    handle: function () {
      bus.$emit("sendLocation",this.start,this.end)
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