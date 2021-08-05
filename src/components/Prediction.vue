<template>
  <div class="col-sm-12 col-md-12 pred">
    <p>Journey Info:</p>
    <div v-if="loading" class="loader-template"></div>
    <div v-else>
    <li v-for="(item,index) in wholeRouteDict" v-bind:key="index">
      {{item.mode}} - {{item.time}} -{{item.instruction}}
      <Notification
          v-if="item.mode=='bus'&&item.trackable==true"
          :stop_dep="item.stop_dep"
          :stop_arr="item.stop_arr"
          :direction="item.direction"
          :route="item.route"
      ></Notification>
    </li>
    </div>
  </div>
</template>

<script>
import Notification from "@/components/Notification";
export default {
  components: {Notification},
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
      this.wholeRouteDict[0]={'mode':'bus','time':data.time, 'instruction':'Take bus'+route,
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
            this.wholeRouteDict[i]={'mode':'walking','time':route.steps[i].duration.value,'instruction':route.steps[i].instructions};
            continue;

          } else if (route.steps[i].travel_mode == 'TRANSIT') {

            if(route.steps[i].transit.line.agencies[0].name!="Dublin Bus"){
              this.wholeRouteDict[i]={'mode':'bus','time':route.steps[i].duration.value,'instruction':route.steps[i].instructions};
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
              this.wholeRouteDict[i]={'mode':'bus','time':res.time,'instruction':route.steps[i].instructions,
              'trackable':res.trackable, 'stop_dep':res.stop_dep, 'stop_arr':res.stop_arr, 'direction':res.direction,
              'route':routeID};
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
    }
  },
};
</script>

<style scoped>
.pred {
  margin-bottom: 20px;
  border-top: 1px solid #fefefe;
}

</style>