<template>
  <div class="col-sm-12 col-md-3">
    <p>Journey Info:</p>
    <div>Time: {{ predict.time }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      predict: {
        time: "test",
      },
    };
  },

  methods: {
    getTripPrediction: async function (route,direction,dep_stop,arr_stop,datetime) {
      const predictionURL = '/predict/'+route+'/'+direction+'/'+dep_stop+'/'+arr_stop+'/'+datetime
      const response = await fetch(predictionURL);
      const data = await response.json();
      this.predict.time = data.time;
    },

    getGooglePrediction: function (route){
        let wholeRouteDict={};
        for(let i=0;i<route.steps.length;i++) {
          let routeDict = {}
          if (route.steps[i].travel_mode == 'WALKING') {
            wholeRouteDict[i]={'walking':route.steps[i].duration.value}
            continue
          } else if (route.steps[i].travel_mode == 'TRANSIT') {
            let routeID = route.steps[i].transit.line.short_name
            let departureStop = route.steps[i].transit.departure_stop.name
            let arrStop = route.steps[i].transit.arrival_stop.name
            let googleTime = route.steps[i].duration.value
            routeDict['routeID'] = routeID
            routeDict['departureStop'] = departureStop
            routeDict['arrStop'] = arrStop
            routeDict['googleTime'] = googleTime
            routeDict['datetime'] = this.timestamp
            this.replacePrediction(routeDict).then(res=>{
              wholeRouteDict[i]={'bus':res}
            })
          }
        }
        console.log(wholeRouteDict)
    },

    replacePrediction: async function (routeList){
      let url="/ptpjourney"
      let response = await fetch(url,{
            method:'POST',
            body:JSON.stringify(routeList),
            headers: new Headers({
            'Content-Type': 'application/json'
          })
          })
      const data = await response.json();
      return data.time
    }
  },
};
</script>

<style>
</style>