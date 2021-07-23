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

  props: {
    
    showMarkers: {
      type: Boolean,
      default: true
    },

    agencyFilter: {
      type: String,
      default: "all"
    },

    routeFilter: {
      type: String,
      default: "all"
    },

    directionFilter: {
      type: String,
      default: "both"
    },

    showVariants: {
      type: Boolean,
      default: false
    }

  },

  watch: {
    showMarkers: "refreshView", 
    agencyFilter: "refreshView",
    routeFilter: "refreshView", 
    directionFilter: "refreshView"
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

      this.refreshView()
    
    },

    fetchData(callback) {

      if (!this.showMarkers)
        callback({})

      else {

        const url = `/stops/${this.agencyFilter}/${this.routeFilter}/info` 

        fetch(url)
        .then(response => response.json())
        .then(callback)

      }

    },

    refreshView() {

      if (this.loading)
        return

      this.loading = true

      this.fetchData((data) => {
        this.stopsData = data
        this.refreshMarkers()
        this.loading = false
      })

    },

    isVisible(stop) {

        for (const route of stop.routes) {
          
          if ( (this.agencyFilter == "all" || route.agency == this.agencyFilter)
            && (this.routeFilter == "all" || route.name == this.routeFilter)
            && (this.directionFilter == "both" || route.direction == this.directionFilter)
            && (this.showVariants || route.main))
            return true

        }

        return false

    },

    refreshMarkers() {

      for (let marker of this.markers)
        marker.setMap(null)

      // Is there a way of clearing an array in javascript
      // that is considered more 'proper'?
      this.markers.splice(0, this.markers.length)

      if (!this.showMarkers)
        return

      for (const stop of Object.values(this.stopsData)) {

        if (this.isVisible(stop)) {

          const marker = new window.google.maps.Marker({
            position: {
              lat: stop.lat,
              lng: stop.lng
            },
            map: this.map
          })

        }

      }

    }
  }
}
</script>
