<template>
<div class="point2point-main">
  <h2>Point-to-point Journey</h2>
  <button
      class="btn btn-warning"
      @click="useCurrentLocation"
  >
    Use current location
  </button>
  <div class="form-group">
  <PlaceInput
      ref="start_input"
      id_name="autocomplete1"
      v-on:sendPlaceID="getStart"
      place_holder="Start location"
  ></PlaceInput>
<!--  id_name is set to differentiate between two placeinput components-->
  </div>
  <div class="form-group">
  <PlaceInput
      id_name="autocomplete2"
      v-on:sendPlaceID="getEnd"
      place_holder="End location"
  ></PlaceInput>
  </div>
  <PointToPointRenderer
      v-on:directionsValidated="showGooglePrediction"
      ref="renderer"
  ></PointToPointRenderer>
  <div class="col-xs-6 col-md-8 datetime">
  <DateTimeInput
      gap="1.5em"
      v-on:sendTimestamp="updateTimestamp"
  ></DateTimeInput>
  </div>
  <div class="col-12">
    <button @click="handle" type="button" class="btn btn-warning">Submit</button>
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

<style scoped>
.point2point-main > div, .point2point-main > button {
  margin-top: 1.5em;
}

.datetime {
  margin: auto;
}
</style>

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
      show_prediction:false
    }
  },

  computed: {
    map() {
      return this.$store.state.map;
    },
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

    useCurrentLocation: function (){
      if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(res => {
          let latlon = {'lat':res.coords.latitude, 'lng':res.coords.longitude}

          if(this.map){
            let geocoder = new window.google.maps.Geocoder();
            geocoder.geocode({ location: latlon }).then((response)=>{

              if (response.results[0]){
                this.$refs.start_input.changeAddress(response.results[0].formatted_address);
                this.start = response.results[0].place_id;
              }
              else{
                alert("Something went wrong with geocoding")
              }
            })
          }
        }
        )
      }
      else{
        alert("Geolocation is not supported by this browser.")
      }
    },

    refreshView: function (){
      this.show_prediction=false;
      this.$refs.renderer.clearView();
      this.$refs.predict.refreshView();
    }
  }
}
</script>
