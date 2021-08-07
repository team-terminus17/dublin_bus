<template>
  <div>
    <Tabs
        v-on:tabChanged="$emit('tabChanged')"
    >
      <Tab name="Tab 1" selected="true">
        <div id="Tab 1" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <div v-html="journey" class="d-flex"></div>
            <div class="col-xs-6 col-md-12">
              <PointToPointJourney
                  v-on:googleQueryComplete="$emit('googleQueryComplete',arguments[0],arguments[1])"
              ></PointToPointJourney>
            </div>
          </div>
        </div>
      </Tab>

      <Tab name="Tab 2">
        <div id="Tab 2" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <StopToStopJourney
                v-on:tripComplete="$emit('tripComplete',arguments[0],arguments[1],arguments[2],arguments[3],arguments[4])"
            ></StopToStopJourney>
          </div>
        </div>
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

export default {
  name: "TripSelection",
  components: {
    Tab,
    Tabs,
    Timeline,
    PointToPointJourney,
    StopToStopJourney
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