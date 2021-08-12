<template>
  <div></div>
</template>

<script>

export default {
  name: "TripRenderer",

  watch: {
    map: "mapUpdated",
  },

  data: function () {
    return {
      busPath: null,
      busPathCoordinates: [],
      markers: []
    };
  },

  computed: {
    map() {
      return this.$store.state.map;
    },
  },

  created() {
    this.updateView();
  },

  beforeDestroy() {
    this.clearView();
  },

  methods: {
    mapUpdated() {
      this.clearView();

      if (this.map) {
        this.busPath = new window.google.maps.Polyline({
          strokeColor: '#1b9cfa',
          strokeOpacity: 0.5,
          strokeWeight: 6,
        });
        this.busPath.setMap(this.map);
      } else {
        this.busPath = null;
      }

      this.updateView();
    },

    clearView() {
      if (this.busPath)
        this.busPath.setPath([]);
      this.map.setZoom(12);
      this.map.setCenter({ lat: 53.3673893, lng: -6.2600157 });
      this.removeMarkers();
    },

    updateView() {
      if (this.busPath)
        this.busPath.setPath(this.busPathCoordinates);
        this.placeMarkers();
    },

    displaySegment(route, stop_dep, stop_arr, direction) {
      fetch(`/shape/${route}/${direction}/${stop_dep}/${stop_arr}`)
          .then(response => response.json())
          .then(data => {
            this.busPathCoordinates=data.coordinates;
            this.updateView();
            this.map.fitBounds(new window.google.maps.LatLngBounds(data.bound[0],data.bound[1]))
    })
    },

    placeMarkers: function (){
      if(this.map){
        const marker_start=new window.google.maps.Marker({
        position:this.busPathCoordinates[0],
        map:this.map,
        label:'A'
      });
      const marker_stop=new window.google.maps.Marker({
        position:this.busPathCoordinates[this.busPathCoordinates.length-1],
        map:this.map,
        label:'B'
      }
      );
      this.markers.push(marker_start);
      this.markers.push(marker_stop);
      }

    },

    removeMarkers: function () {
      for (let marker of this.markers) marker.setMap(null);
      this.markers = [];
    },
  },
};
</script>
