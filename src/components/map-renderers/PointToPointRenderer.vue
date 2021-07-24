<template>
  <div></div>
</template>

<script>
import bus from "@/components/bus";

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

  mounted() {
    bus.$on("showDirection", this.showDirection);
    bus.$on("sendLocation", this.getGoogleTime); //get from PlaceInput component
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
      if (this.directionsRenderer) this.directionsRenderer.setDirections(null);
    },

    updateView() {
      if (this.directionsRenderer)
        this.directionsRenderer.setDirections(this.directions);
    },

    showDirection() {
      if (!this.directionsService) return;

      let request = {
        origin: { lat: arguments[0].lat, lng: arguments[0].lng },
        destination: { lat: arguments[1].lat, lng: arguments[1].lng },
        travelMode: "TRANSIT",
        transitOptions: {
          modes: ["BUS"], // Specifies that we only want Dublin Bus to be considered
        },
      };

      this.directionsService.route(request, (response, status) => {
        if (status == "OK") this.directions = response;
        else this.directions = null;
      });

      this.updateView();
    },

    getGoogleTime: function () {
      if (!this.directionsService) return;

      let timestamp = 1626768540000; // A place holder, need to be changed when combined with time input

      let request = {
        origin: { placeId: arguments[0] },
        destination: { placeId: arguments[1] },
        travelMode: "TRANSIT",
        transitOptions: {
          modes: ["BUS"], // Specifies that we only want Dublin Bus to be considered
          routingPreference: "FEWER_TRANSFERS",
          departureTime: new Date(timestamp),
        },
      };

      this.directionsService.route(request, (response, status) => {
        let route = response.routes[0].legs[0];
        let routeList = [];
        let walkingTime = 0;

        for (let i = 0; i < route.steps.length; i++) {
          let routeDict = {};

          if (route.steps[i].travel_mode == "WALKING") {
            walkingTime += route.steps[i].duration.value;
            continue;
          } else if (route.steps[i].travel_mode == "TRANSIT") {
            let routeID = route.steps[i].transit.line.short_name.toLowerCase();
            let departureStop = route.steps[i].transit.departure_stop.name;
            let arrStop = route.steps[i].transit.arrival_stop.name;
            let googleTime = route.steps[i].duration.value;

            routeDict["routeID"] = routeID;
            routeDict["departureStop"] = departureStop;
            routeDict["arrStop"] = arrStop;
            routeDict["googleTime"] = googleTime;
            routeDict["datetime"] = timestamp;

            routeList.push(routeDict);
          }
        }

        this.getPrediction(routeList);
        if (status == "OK") this.directions = response;
        else this.directions = null;

        this.updateView();
      });
    },

    //We could probably move this to prediction component(i.e if we click the submit button of different tab it will trigger corresponding function to get the prediction time)
    getPrediction: async function (routeList) {
      let url = "/ptpjourney";
      let response = await fetch(url, {
        method: "POST",
        body: JSON.stringify(routeList),
        headers: new Headers({
          "Content-Type": "application/json",
        }),
      });
      const data = await response.json();
    },
  },
};
</script>
