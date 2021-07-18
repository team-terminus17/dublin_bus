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
    bus.$on("sendLocation",this.getGoogleTime)//get from PlaceInput component
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
      //Send to PlaceInput component. This is to ensure that google is loaded before the autocomplete is used.
      //Will come back to it if I've got a better solution
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
      },

    getGoogleTime: function (){
      let timestamp=1626768540000// A place holder, need to be changed when combined with time input
      let request={
        origin:{placeId:arguments[0]},
        destination:{placeId:arguments[1]},
        travelMode: 'TRANSIT',
        transitOptions: {
            modes: ['BUS'], // Specifies that we only want Dublin Bus to be considered
            routingPreference: 'FEWER_TRANSFERS',
            departureTime: new Date(timestamp),
        },
      };
      this.directionsService.route(request, (response, status) =>  {
        let route=response.routes[0].legs[0];
        console.log(route)
        let walkingTime=0;
        let routeList=[];
        for(let i=0;i<route.steps.length;i++) {
          let routeDict = {}
          if (route.steps[i].travel_mode == 'WALKING') {
            walkingTime += route.steps[i].duration.value
            continue
          } else if (route.steps[i].travel_mode == 'TRANSIT') {
            let routeID = route.steps[i].transit.line.short_name.toLowerCase()
            let departureStop = route.steps[i].transit.departure_stop.name
            let arrStop = route.steps[i].transit.arrival_stop.name
            let googleTime = route.steps[i].duration.value
            routeDict['routeID'] = routeID
            routeDict['departureStop'] = departureStop
            routeDict['arrStop'] = arrStop
            routeDict['googleTime'] = googleTime
            routeDict['datetime'] = timestamp
            routeList.push(routeDict)
          }
        }
        console.log(routeList)
        this.getPrediction(routeList)
      if (status == 'OK') {
        this.directionsRenderer.setDirections(response);
      }
    });
    },

    getPrediction: async function (routeList){
      let url="/ptpjourney"
      let response = await fetch(url,{
            method:'POST',
            body:JSON.stringify(routeList),
            headers: new Headers({
            'Content-Type': 'application/json'
          })
          })
      const data = await response.json();
      console.log(data.time);
    }

    }
}
</script>
