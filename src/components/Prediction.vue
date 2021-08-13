<template>
  <div class="col-sm-12 col-md-12 pred">
    <p style="font-size: larger;font-weight: bolder">Journey Info</p>
    <div v-if="loading" class="loading-content">
      <div class="loader-template"></div>
    </div>
    <div v-else>
    <div v-for="(item,index) in wholeRouteDict" v-bind:key="index">
      <JourneyInfoBox
      :item="item">
      </JourneyInfoBox>
    </div>
    </div>
  </div>
</template>

<script>
import Notification from "@/components/Notification";
import JourneyInfoBox from "@/components/JourneyInfoBox";
import {round} from "@popperjs/core/lib/utils/math";
export default {
  components: {JourneyInfoBox},
  data() {
    return {
      predict: {
        time: "test",
      },
      wholeRouteDict: {},
      loading: false,
    };
  },

  methods: {
    refreshView: function (){
      this.wholeRouteDict={};
      this.$forceUpdate();
    },

    getTripPrediction: async function (route,direction,dep_stop,arr_stop,datetime) {
      this.refreshView();
      this.loading=true
      const predictionURL = `/predict/${route}/${direction}/${dep_stop}/${arr_stop}/${datetime}`
      const response = await fetch(predictionURL);
      const data = await response.json();
      let time = this.secondToMinute(data.time);

      this.wholeRouteDict[0]={'mode':'bus','time':time,
      'trackable':true, 'stop_dep':dep_stop, 'stop_arr':arr_stop, 'direction':direction, 'route':route};
      this.loading=false;
      this.$forceUpdate();
    },

    getGooglePrediction: async function (route, timestamp){
      this.refreshView();
      this.loading = true
       for(let i=0;i<route.steps.length;i++) {
          let routeDict = {};

          if (route.steps[i].travel_mode == 'WALKING') {
            this.wholeRouteDict[i]={'mode':'walking','time':this.secondToMinute(route.steps[i].duration.value),
              'instruction':route.steps[i].instructions};
            continue;

          } else if (route.steps[i].travel_mode == 'TRANSIT') {
            let instruction='';
            let start = route.steps[i]['transit']['departure_stop']['name'];
            let end = route.steps[i]['transit']['arrival_stop']['name'];
            instruction += `<div>${start}</div>`
            instruction += '<div>To<div>'
            instruction += `<div>${end}<div>`
            if(route.steps[i].transit.line.agencies[0].name!="Dublin Bus"){
              this.wholeRouteDict[i]={'mode':'bus','time':this.secondToMinute(route.steps[i].duration.value),
                'instruction':instruction,'busroute':route.steps[i]['transit']['line']['short_name']};
              continue;
            }

            let routeID = route.steps[i].transit.line.short_name;
            let departureStop = route.steps[i].transit.departure_stop.name;
            let arrStop = route.steps[i].transit.arrival_stop.name;
            let googleTime = route.steps[i].duration.value;
            routeDict['routeID'] = routeID;
            routeDict['departureStop'] = departureStop;
            routeDict['arrStop'] = arrStop;
            routeDict['googleTime'] = googleTime;
            routeDict['datetime'] = timestamp;
            await this.replacePrediction(routeDict).then(res=>{
              let time = this.secondToMinute(res.time);
              this.wholeRouteDict[i]={'mode':'bus','time':time,'instruction':instruction,
              'trackable':res.trackable, 'stop_dep':res.stop_dep, 'stop_arr':res.stop_arr, 'direction':res.direction,
              'route':routeID,'busroute':route.steps[i]['transit']['line']['short_name']};
            })
          }
        }
       this.loading=false
        this.$forceUpdate();
    },

    replacePrediction: async function (routeList){
      let url="/ptpjourney";
      let response = await fetch(url,{
            method:'POST',
            body:JSON.stringify(routeList),
            headers: new Headers({
            'Content-Type': 'application/json'
          })
          })
      const data = await response.json();
      return data;
    },

    secondToMinute: function (second){
      return round(second/60).toString()+' mins';
    },

  },
};
</script>

<style scoped>
.pred {
  color: #1b1b1b;
  margin-bottom: 20px;
  border: 2px solid var(--border-color);
  background-color: var(--background-color);
  border-radius: var(--border-radius);
  overflow: auto;
  max-height: 300px;
}
.loading-content {
  height: 10em;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>