<template>
<div>
  <div class="form-group" style="margin-top: 6px">
  <PlaceInput
      id_name="autocomplete1"
      v-on:sendPlaceID="getStart"
      place_holder="Enter the start location"
  ></PlaceInput>
<!--  id_name is set to differentiate between two placeinput components-->
  </div>
  <div class="form-group" style="margin-top: 10px">
  <PlaceInput
      id_name="autocomplete2"
      v-on:sendPlaceID="getEnd"
      place_holder="Enter the end location"
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
  <div class="col-12" style="margin-bottom: 10px">
  <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 40px;">Submit</button>
  </div>
  <div v-show="show_prediction">
  <div class="col-12">
  <Prediction
      ref="predict"
      :mode="mode"
  ></Prediction>
  </div>
  </div>
</div>
</template>

<script>
import PlaceInput from "@/components/PlaceInput";
import PointToPointRenderer from "@/components/map-renderers/PointToPointRenderer";
import DateTimeInput from "@/components/DateTimeInput";
import Prediction from "@/components/Prediction";
export default {
  name: "PointToPointJourney",

  props:['mode'],

  components: {
    Prediction,
    PointToPointRenderer,
    PlaceInput,
    DateTimeInput
  },

  data(){
    return{
      start:null,
      end:null,
      timestamp:null,
      show_prediction:false,
    }
  },

  methods: {
    handle: function () {
      if(this.start==null||this.end==null){
        alert("You need to enter both origin and destination.");
      }
      else{
        this.show_prediction=true;
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
      this.$refs.predict.getGooglePrediction(route,this.timestamp);
    },

    updateTimestamp: function (val){
      this.timestamp = val;
    },

    refreshView: function (){
      this.show_prediction=false;
      this.$refs.renderer.clearView();
      this.$refs.predict.refreshView();
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
  border: 1px solid var(--border-color);
  width: 100%;
  outline: none;
  background-color: var(--background-color);
  border-radius: var(--border-radius);
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
  border-bottom: 1px solid var(--border-color);
  border-radius: var(--border-radius);
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item{
  cursor: pointer;
  color: black;
  background-color: #bbdaa4;
  padding: 10px;
  border-bottom: 1px solid var(--border-color);
  border-left: 1px solid var(--border-color);
  border-right: 1px solid var(--border-color);
  text-align: center;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item:hover{
  background-color: #bbd7f2;
}

.v-autocomplete .v-autocomplete-list .v-autocomplete-list-item.v-autocomplete-item-active {
  background-color:	#bbd7f2;
}


.datetime {
  margin-left: 16%;
}

@media only screen and (max-width: 600px) {
  .datetime {
    margin-left: 0%;
  }
}

</style>