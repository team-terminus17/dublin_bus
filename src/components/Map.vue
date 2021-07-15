<template>
  <div>
    <div id="map"
    style="width: 100%;height: 500px"
    >
    </div>
  </div>
</template>

<script>
import bus from "@/components/bus";
export default {
  name: "Map",
  data(){
    return{
      map:null,
      directionsRenderer:null,
      directionsService:null
    }
  },
  created() {
    window.checkAndAttachMapScript(this.initMap);
  },
  mounted() {
    bus.$on("showDirection",this.showDirection)
  },
  methods:{
    initMap(){
      this.map= new window.google.maps.Map(document.getElementById("map"),{
        center: {lat: 53.3673893, lng: -6.2600157},
        zoom: 12,
      });
      this.directionsRenderer = new window.google.maps.DirectionsRenderer();
      this.directionsService = new window.google.maps.DirectionsService();
      this.directionsRenderer.setMap(this.map);
      bus.$emit("sendGoogle",window.google);
    },
    showDirection(){
      let request = {
      origin: { lat:arguments[0].lat, lng:arguments[0].lng},
      destination: { lat: arguments[1].lat, lng:arguments[1].lng },
      travelMode: 'TRANSIT',
          transitOptions: {
              modes: ['BUS'], // Specifies that we only want Dublin Bus to be considered
          }
    };
      this.directionsService.route(request, (response, status) =>  {
      if (status == 'OK') {
        this.directionsRenderer.setDirections(response);
      }
    });
      }

    }
}
</script>
