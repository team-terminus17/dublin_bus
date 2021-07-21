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

  props: {
    
    showMarkers: {
      type: Boolean,
      default: true
    },

    agencyFilter: String,
    routeFilter: String,
    directionFilter: String

  },

  data(){
    return{
      map: null,
      loading: false,
      stopsData: null,
      markers: []
    }
  },

  created() {
    window.checkAndAttachMapScript(this.initMap);
  },

  methods:{
    
    initMap() {
      
      this.map= new window.google.maps.Map(document.getElementById("map"),{
        center: {lat: 53.3673893, lng: -6.2600157},
        zoom: 12,
      });

      this.refreshMarkers()
    
    },

    fetchData() {

      this.loading = true

      fetch(`/stops/all/coordinates`)
      .then(response => response.json())
      .then(data => {
        
        this.stopsData = data
        this.loading = false
        this.refreshMarkers()

      })

    },

    refreshMarkers() {

      if (this.loading)
        return

      if (!this.stopsData) {
        this.fetchData()
        return
      }

      this.loading = true

      for (let marker of this.markers)
        marker.setMap(null)

      // Is there a way of clearing an array in javascript
      // that is considered more 'proper'?
      this.markers.splice(0, this.markers.length)

      if (!this.showMarkers)
        return

      console.log("Populating map")

      for (const stop of Object.values(this.stopsData)) {

        const test = new window.google.maps.LatLng(53.3473, -6.2625)

        const marker = new window.google.maps.Marker({
          position: {
            lat: stop.lat,
            lng: stop.lng
          },
          map: this.map,
          visible: true
        })

      }

      console.log("Done")
    }
  }
}
</script>
