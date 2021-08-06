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
      busPathCoordinates: []
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
          strokeColor: '#FFB266',
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
    },

    updateView() {
      if (this.busPath)
        this.busPath.setPath(this.busPathCoordinates);
    },

    displaySegment(route, stop_dep, stop_arr, direction) {
      fetch(`/shape/${route}/${direction}/${stop_dep}/${stop_arr}`)
          .then(response => response.json())
          .then(data => {
            this.busPathCoordinates=data.coordinates;
            this.updateView();
            console.log(data.bound)
            this.map.fitBounds(new window.google.maps.LatLngBounds(data.bound[0],data.bound[1]))
    })
    }
  },
};
</script>
