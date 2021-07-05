<template>
  <div>
    <div id="map"
    style="width: 100%;height: 500px"
    >
    </div>
  </div>
</template>

<script>
export default {
  name: "Map",
  data(){
    return{
      map:null,
    }
  },
  mounted() {
    window.checkAndAttachMapScript(this.initMap)
  },
  methods:{
    initMap(){
      this.map= new window.google.maps.Map(document.getElementById("map"),{
        center: {lat: 53.3673893, lng: -6.2600157},
        zoom: 12,
      });
    },
    // showDirection(){
    //
    // }
  }
}
</script>
