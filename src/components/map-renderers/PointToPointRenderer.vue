<template>
  <div></div>
</template>

<script>

export default {
  name: "PointToPointRenderer",

  watch: {
    map: "mapUpdated",
  },

  data: function () {
    return {
      directionsService: null,
      directionsRenderer: null,
      directions: null,
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
        this.directionsService = new window.google.maps.DirectionsService();
        this.directionsRenderer = new window.google.maps.DirectionsRenderer();
        this.directionsRenderer.setMap(this.map);
      } else {
        this.directionsService = null;
        this.directionsRenderer = null;
      }

      this.updateView();
    },

    clearView() {
      if (this.directionsRenderer)
        this.directionsRenderer.setDirections(null);
      //Although it is functioning, I don't know why the console in chrome devtools would give me an error
      //"InvalidValueError: setDirections: not an Object"
    },

    updateView() {
      if (this.directionsRenderer)
        this.directionsRenderer.setDirections(this.directions);
    },

    getGoogleTime: function (start, end, timestamp) {
      if (!this.directionsService) return;

      let request={
        origin:{placeId:start},
        destination:{placeId:end},
        travelMode: 'TRANSIT',
        transitOptions: {
            modes: ['BUS'], // Specifies that we only want Dublin Bus to be considered
            routingPreference: 'FEWER_TRANSFERS',
            departureTime: new Date(timestamp*1000),
        },
      };
      this.directionsService.route(request, (response, status) =>  {
      if (status == 'OK') {
        this.directions=response;
        let route=response.routes[0].legs[0];
        this.$emit("directionsvalidified",route)
      }
      else{
        this.directions=null;
        alert("Bus is resting now")
      }
      this.updateView();
      });
    },

  },
};
</script>
