<template>
  <div>
    <Tabs
        v-on:tabChanged="onTabChanged"
        :mode="mode"
    >
      <Tab name="Point To Point Journey" selected="true" :img_link="img_link[0]">
        <div id="Tab 1" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <div v-html="journey" class="d-flex"></div>
            <div class="col-xs-6 col-md-12">
              <PointToPointJourney
                  v-on:googleQueryComplete="$emit('googleQueryComplete',arguments[0],arguments[1])"
                  ref="ptpjourney"
                  :mode="mode"
              ></PointToPointJourney>
            </div>
          </div>
        </div>
      </Tab>

      <Tab name="Stop To Stop Journey" :img_link="img_link[1]">
        <div id="Tab 2" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <StopToStopJourney
                v-on:tripComplete="$emit('tripComplete',arguments[0],arguments[1],arguments[2],arguments[3],arguments[4])"
                ref="stsjourney"
                :mode="mode"
            ></StopToStopJourney>
          </div>
        </div>
      </Tab>
      
      <Tab name="Realtime" :img_link="img_link[2]">
        <RealtimeView
            ref="realtime"
        ></RealtimeView>
      </Tab>

      <Tab name="Twitter" :img_link="img_link[3]">
        <Twitter
            :mode="mode"
        ></Twitter>
      </Tab>
    </Tabs>
  </div>
</template>

<script>
import Tab from "@/components/Tab";
import Tabs from "@/components/Tabs";
import PointToPointJourney from "@/components/PointToPointJourney";
import StopToStopJourney from "@/components/StopToStopJourney";
import RealtimeView from "@/components/RealtimeView.vue"
import Twitter from "@/components/Twitter";

export default {
  name: "TripSelection",

  props:['mode'],

  components: {
    Twitter,
    Tab,
    Tabs,
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
      routeinfo: null,
      img_link: [
        {'light':'https://img.icons8.com/material/48/000000/location-update.png',
        'dark':'https://img.icons8.com/material-rounded/48/ffffff/worldwide-location.png'},
        {'light':'https://img.icons8.com/fluency-systems-regular/48/000000/bus-stop.png',
        'dark':'https://img.icons8.com/fluency-systems-regular/48/ffffff/bus-stop.png'},
        {'light':'https://img.icons8.com/material-outlined/48/000000/wall-clock.png',
        'dark':'https://img.icons8.com/material-outlined/48/ffffff/wall-clock.png'},
        {'light':'https://img.icons8.com/material-outlined/48/000000/twitter.png',
        'dark':'https://img.icons8.com/material-outlined/48/ffffff/twitter.png'}],
    }
  },
  methods:{
    onTabChanged: function (){
      this.$emit('tabChanged');
      this.$refs.ptpjourney.refreshView();
      this.$refs.stsjourney.refreshView();
      this.$refs.realtime.refreshView();
    },

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