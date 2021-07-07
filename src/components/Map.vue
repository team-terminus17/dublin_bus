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
    }
  },
  mounted() {
    window.checkAndAttachMapScript(this.initMap);
    bus.$on("showDirection",this.showDirection)
  },
  methods:{
    initMap(){
      this.map= new window.google.maps.Map(document.getElementById("map"),{
        center: {lat: 53.3673893, lng: -6.2600157},
        zoom: 12,
      });
    },
    showDirection(){
      if(window.google){
        let directionsService = new window.google.maps.DirectionsService();
      let directionsRenderer = new window.google.maps.DirectionsRenderer();
      directionsRenderer.setMap(this.map);
      let request = {
      origin: { lat:arguments[0].lat, lng:arguments[0].lng},
      destination: { lat: arguments[1].lat, lng:arguments[1].lng },
      travelMode: 'TRANSIT',
          transitOptions: {
              modes: ['BUS'], // Specifies that we only want Dublin Bus to be considered
          }
    };
      directionsService.route(request, function(result, status) {
      if (status == 'OK') {
        directionsRenderer.setDirections(result);
      }
    });
      }

    }
  }
}
</script>
