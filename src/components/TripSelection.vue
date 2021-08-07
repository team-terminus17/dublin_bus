<template>
  <div>
    <Tabs>
      <Tab name="Tab 1" selected="true">
        <div id="Tab 1" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <div v-html="journey" class="d-flex"></div>
            <div class="col-xs-6 col-md-12">
              <PointToPointJourney></PointToPointJourney>
            </div>
          </div>
        </div>
      </Tab>

      <Tab name="Tab 2">
        <div id="Tab 2" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <StopToStopJourney></StopToStopJourney>
          </div>
        </div>
      </Tab>
      
      <Tab name="Realtime">
        <RealtimeView></RealtimeView>
      </Tab>

      <Tab name="Twitter">
        <Timeline id="dublinbusnews" sourceType="profile" widget-class="twitter"/>
      </Tab>
    </Tabs>
  </div>
</template>

<script>
import Tab from "@/components/Tab";
import Tabs from "@/components/Tabs";
import {Timeline} from "vue-tweet-embed";
import PointToPointJourney from "@/components/PointToPointJourney";
import StopToStopJourney from "@/components/StopToStopJourney";
import RealtimeView from "@/components/RealtimeView.vue"

export default {
  name: "TripSelection",
  components: {
    Tab,
    Tabs,
    Timeline,
    PointToPointJourney,
    StopToStopJourney,
    RealtimeView,
  },
  data() {
    return {
      valid: false,
      route: null,
      stop_dep: null,
      stop_arr: null,
      journey: "Please input your journey info:",
      origin: null,
      destination: null,
      direction: null,
      routeinfo: null
    }
  },
  methods:{
    getRoutes:async function(){
      let url = `/coordinate/${this.direction}/${this.route}/${this.stop_dep}/${this.stop_arr}`;
      let response = await fetch(url);
      let data = await response.json();

      if(data['valid']==2){
        alert("Origin and destination can't be the same");
        this.valid = false;
        return;
      }
      if (data["valid"] == 1) {
        alert("The selected route is not in the same direction");
        this.valid = false;
        return;
      }
      this.valid=true;
      this.origin = {lat: data['stop_dep']['lat'],lng:data['stop_dep']['lon']}
      this.destination = {lat: data['stop_arr']['lat'],lng:data['stop_dep']['lon']}
      this.$emit("tripComplete",this.route,this.direction,this.stop_dep,this.stop_arr)
  },

    handle() {
      if (this.stop_arr == null || this.stop_dep == null) {
        alert("Please fill in the complete route");
        return;
      }
      this.getRoutes();
      this.$refs.renderer.displaySegment(this.route,this.stop_dep,this.stop_arr,this.direction);
  },

    getRoute: function (){
      this.route=arguments[0];
      this.direction=arguments[1];
      this.routeinfo=arguments;
    },

    getDepStop: function (val){
      this.stop_dep=val;
    },

    getArrStop: function (val){
      this.stop_arr=val;
  }
  },

}
</script>

<style scoped>


.twitter {
  max-height: 450px;
  overflow-y: auto;
}

@media only screen and (max-width: 600px) {

}
</style>