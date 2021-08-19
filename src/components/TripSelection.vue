<template>
  <div>
    <Tabs
        v-on:tabChanged="onTabChanged"
    >
      <Tab name="Tab 1" selected="true">
        <div id="Tab 1" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <div class="col-xs-6 col-md-12">
              <PointToPointJourney
                  v-on:googleQueryComplete="$emit('googleQueryComplete',arguments[0],arguments[1])"
                  ref="ptpjourney"
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
            ></StopToStopJourney>
          </div>
        </div>
      </Tab>
      
      <Tab name="Realtime">
        <RealtimeView></RealtimeView>
      </Tab>

      <Tab name="Twitter">
        <h2>Twitter</h2>
        <Timeline id="dublinbusnews" sourceType="profile" widget-class="twitter" :options="{ theme: 'light' }"/>
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
      origin: null,
      destination: null,
      direction: null,
      routeinfo: null
    }
  },
  methods:{
    onTabChanged: function (){
      this.$emit('tabChanged');
      this.$refs.ptpjourney.refreshView();
      this.$refs.stsjourney.refreshView();
    },

    test() {
      console.log('test')
      document.getElementById('dublinbusnews'),
      {
        options:"{ theme: 'dark' }"
      }
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