<template>
  <div>
    <Tabs
        v-on:tabChanged="onTabChanged"
    >
      <Tab name="Tab 1" selected="true">
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

      <Tab name="Tab 2">
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
      
      <Tab name="Realtime">
        <RealtimeView
            ref="realtime"
        ></RealtimeView>
      </Tab>

      <Tab name="Twitter">
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
    }
  },
  methods:{
    onTabChanged: function (){
      this.$emit('tabChanged');
      this.$refs.ptpjourney.refreshView();
      this.$refs.stsjourney.refreshView();
      this.$refs.realtime.refreshView();
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