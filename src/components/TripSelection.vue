<template>
  <div>
    <Tabs>
      <Tab name="Tab 1" selected="true">
        <div id="Tab 1" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <div v-html="journey" class="d-flex"></div>
            <!-- <div
              class="col-md-4 justify-content-space-between"
              style="margin-top: 20px"
            >
              <label class="d-flex justify-content-start"
                >Route Selection</label
              >
              <RouteSelection v-on:selectRoute="getRoute"></RouteSelection>
            </div> -->
            <div class="col-md-12 align-self-end" style="font-size: 90%;">
              <label style="margin-right: 5px; margin-left: -20px; margin-top: 20px;"
                >Inbound</label
              >
              <label class="switch">
                <input type="checkbox" />
                <span class="slider"></span>
              </label>
              <label style="margin-right: -5px; margin-left: 5px"
                >Outbound</label
              >
            </div>
            <div class="col-xs-6 col-md-12">
              <div class="form-group" style="margin-top: 6px">
                <label class="d-flex justify-content-start">Start location</label>
                <StopSelection v-on:stopSelected="getDepStop"></StopSelection>
              </div>
              <div class="form-group" style="margin-top: 10px">
                <label class="d-flex justify-content-start"
                  >End location</label
                >
                <StopSelection v-on:stopSelected="getArrStop"></StopSelection>
              </div>
            </div>
            <div class="col-xs-6 col-md-12" style="margin-top: 10px">
              <div style="margin-top: 20px">
                <DateInput v-model="date"></DateInput>
              </div>
              <div style="margin-top: 20px">
                <TimeInput v-model="time"></TimeInput>
              </div>
            </div>
            <div id="submit" class="col-md-12" style="margin-bottom: 15px">
              <button
                @click="handle"
                type="button"
                class="btn btn-warning"
                style="margin-top: 30px"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      </Tab>

      <Tab name="Tab 2">
        <div id="Tab 2" class="col-sm-12 col-md-12 tabcontent">
          <div class="row">
            <div v-html="journey" class="d-flex"></div>
            <div
              class="col-md-4 justify-content-space-between"
              style="margin-top: 20px"
            >
              <label class="d-flex justify-content-start"
                >Route Selection</label
              >
              <RouteSelection v-on:selectRoute="getRoute"></RouteSelection>
            </div>
            <div class="col-md-8 align-self-end"  style="font-size: 90%;">
              <label style="margin-right: 5px; margin-left: -20px"
                >Inbound</label
              >
              <label class="switch">
                <input type="checkbox" />
                <span class="slider"></span>
              </label>
              <label style="margin-right: -5px; margin-left: 5px"
                >Outbound</label
              >
            </div>
            <div class="col-md-12">
              <div class="form-group" style="margin-top: 6px">
                <label class="d-flex justify-content-start">Start Stop</label>
                <StopSelection v-on:stopSelected="getDepStop"></StopSelection>
              </div>
              <div class="form-group" style="margin-top: 10px">
                <label class="d-flex justify-content-start"
                  >End Stop</label
                >
                <StopSelection v-on:stopSelected="getArrStop"></StopSelection>
              </div>
            </div>
            <div class="col-md-12" style="margin-top: 10px">
              <div style="margin-top: 20px">
                <DateInput v-model="date"></DateInput>
              </div>
              <div style="margin-top: 20px">
                <TimeInput v-model="time"></TimeInput>
              </div>
            </div>
            <div id="submit" class="col-md-12" style="margin-bottom: 15px">
              <button
                @click="handle"
                type="button"
                class="btn btn-warning"
                style="margin-top: 30px"
              >
                Submit
              </button>
            </div>
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
import Vue from "vue";
import Component from "vue-class-component";
import bus from "@/components/bus";
import RouteSelection from "@/components/RouteSelection";
import StopSelection from "@/components/StopSelection";
import DateInput from "@/components/DateInput";
import TimeInput from "@/components/TimeInput";
import Tab from "@/components/Tab";
import Tabs from "@/components/Tabs";
import Timeline from "vue-tweet-embed";

export default {
  name: "TripSelection",
  components: {
    RouteSelection,
    StopSelection,
    DateInput,
    TimeInput,
    Tab,
    Tabs,
    // Tweet,
    Timeline
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
      time: "3:15",
      date: "2019-09-07",
    };
  },
  methods: {
    getRoutes: async function () {
      let url =
        "/coordinate/" +
        "/" +
        this.route +
        "/" +
        this.stop_dep +
        "/" +
        this.stop_arr;
      let response = await fetch(url);
      let data = await response.json();
      if (data["valid"] == 2) {
        alert("Origin and destination can't be the same");
        this.valid = false;
        return;
      }
      if (data["valid"] == 1) {
        alert("The selected route is not in the same direction");
        this.valid = false;
        return;
      }
      this.valid = true;
      this.origin = {
        lat: data["stop_dep"]["lat"],
        lng: data["stop_dep"]["lon"],
      };
      this.destination = {
        lat: data["stop_arr"]["lat"],
        lng: data["stop_dep"]["lon"],
      };
      bus.$emit("showDirection", this.origin, this.destination);
    },
    handle() {
      if (this.stop_arr == null || this.stop_dep == null) {
        alert("Please fill in the complete route");
        return;
      }
      this.getRoutes();
    },
    getRoute: function (val) {
      this.route = val;
    },
    getDepStop: function (val) {
      this.stop_dep = val;
    },
    getArrStop: function (val) {
      this.stop_arr = val;
    },


  // Attempt to have the date/time selector start with the current date/time
  getDate() {
    var currentdate = new Date();
    var fulldate = currentdate.getFullYear() + "-" + currentdate.getMonth() + "-" + currentdate.getDay();
    var fulltime = currentdate.getHours() + ":" + currentdate.getMinutes();

    this.date = fulldate;
    this.time = fulltime;
    console.log(fulltime)
    console.log(fulldate)
  },

  },

  created() {
    // Call the getDate method on start up
    // this.getDate();
  },
};
</script>

<style scoped>
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
  
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;

}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color:#a7cdf2;
  -webkit-transition: 0.4s;
  transition: 0.4s;
  border-radius: 8px;
  border: 1px solid #157977;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #bbdaa4;
}

input:focus + .slider {
  box-shadow: 0 0 1px #bbdaa4;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

.twitter {
  max-height: 450px;
  overflow-y: auto;
}

@media only screen and (max-width: 600px) {

}
</style>