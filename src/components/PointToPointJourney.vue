<template>
<div>
  <PlaceInput
      id_name="autocomplete1"
      v-on:sendPlaceID="getStart"
      :google="google"
  ></PlaceInput>
<!--  id_name is set to differentiate between two placeinput components-->
  <PlaceInput
      id_name="autocomplete2"
      v-on:sendPlaceID="getEnd"
      :google="google"
  ></PlaceInput>
  <button @click="handle" type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
</div>
</template>

<script>
import PlaceInput from "@/components/PlaceInput";
export default {
  name: "PointToPointJourney",

  components: {
    PlaceInput
  },

  props:['google','map','timestamp'],

  data(){
    return{
      start:null,
      end:null,
      directionsRenderer:null,
      directionsService:null
    }
  },

  watch:{
    google(){
      this.directionsRenderer = new window.google.maps.DirectionsRenderer();
      this.directionsService = new window.google.maps.DirectionsService();
    },

    map(){
      this.directionsRenderer.setMap(this.map);
    }
  },

  methods: {
    handle: function () {
      if(this.start==null||this.end==null){
        alert("You need to enter both origin and destination.")
      }
      else{
        this.renderRoute();
        // bus.$emit("sendLocation",this.start,this.end)//emit to map component
      }
    },

    getStart: function (val){
      this.start=val
    },

    getEnd: function (val){
      this.end=val
    },

    renderRoute:function (){
      let request={
        origin:{placeId:this.start},
        destination:{placeId:this.end},
        travelMode: 'TRANSIT',
        transitOptions: {
            modes: ['BUS'], // Specifies that we only want Dublin Bus to be considered
            routingPreference: 'FEWER_TRANSFERS',
            departureTime: new Date(this.timestamp*1000),
        },
      };
      this.directionsService.route(request, (response, status) =>  {
      if (status == 'OK') {
        this.directionsRenderer.setDirections(response);
        let route=response.routes[0].legs[0];
        this.$emit("googlequerycomplete",route)
      }
      else{
        alert("Bus is resting now")
      }
    });
    }
  }
}
</script>

<style scoped>

</style>