<template>
<div>
  <div class="form-group" style="margin-top: 6px">
  <label class="d-flex justify-content-start">Start location</label>
  <PlaceInput
      id_name="autocomplete1"
      v-on:sendPlaceID="getStart"
  ></PlaceInput>
<!--  id_name is set to differentiate between two placeinput components-->
  </div>
  <div class="form-group" style="margin-top: 10px">
  <label class="d-flex justify-content-start">End location</label>
  <PlaceInput
      id_name="autocomplete2"
      v-on:sendPlaceID="getEnd"
  ></PlaceInput>
  </div>
  <PointToPointRenderer
      v-on:directionsValidated="showGooglePrediction"
      ref="renderer"
  ></PointToPointRenderer>
  <div class="col-xs-6 col-md-12" style="margin-top: 10px">
  <DateTimeInput
      v-on:sendTimestamp="updateTimestamp"
  ></DateTimeInput>
  </div>
  <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
</div>
</template>

<script>
import PlaceInput from "@/components/PlaceInput";
import PointToPointRenderer from "@/components/map-renderers/PointToPointRenderer";
import DateTimeInput from "@/components/DateTimeInput";
export default {
  name: "PointToPointJourney",

  components: {
    PointToPointRenderer,
    PlaceInput,
    DateTimeInput
  },

  data(){
    return{
      start:null,
      end:null,
      timestamp:null,
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
      this.$emit("googleQueryComplete",route,this.timestamp);
    },

    updateTimestamp: function (val){
      this.timestamp = val;
    }
  }
}
</script>

<style scoped>

.v-autocomplete .v-autocomplete-input-group .v-autocomplete-input {
  position: relative;
  font-size: 1.0em;
  padding: 5px 15px;
  box-shadow: none;
  border: 1px solid #157977;
  width: 100%;
  outline: none;
  background-color: 	#bbd7f2;
  border-radius: 8px;
  }

.v-autocomplete .v-autocomplete-list{
  z-index: 1000;
  width: 100%;
  height: 200px;
  overflow-y:auto;
  overflow-x: hidden;
  text-align: left;
  border: none;
  border-top: none;
  max-height: 400px;
  overflow-y: auto;
  border-bottom: 1px solid #157977;
  border-radius: 8px;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item{
  cursor: pointer;
  color: black;
  background-color: #bbdaa4;
  padding: 10px;
  border-bottom: 1px solid #157977;
  border-left: 1px solid #157977;
  border-right: 1px solid #157977;
  text-align: center;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item:hover{
  background-color: 	#bbd7f2;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item.v-autocomplete-item-active {
  background-color:	#bbd7f2;
}

</style>