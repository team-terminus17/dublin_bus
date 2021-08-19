<template>
  <div class="main d-flex flex-column">
    <DarkMode class="dark-mode-toggle"
        v-on:changeMode="changeMode"
    ></DarkMode>
    <div class="content row">
      <div class="col-sm-6 col-md-6 d-flex
        justify-content-start">
        <img src="./assets/team2.png">
      </div>
      <div
      class="
        col-xs-6
        col-sm-6
        col-lg-6
        d-flex
        justify-content-end
        
      "
      id="weather"
    >
         <Weather></Weather>
      </div>
    </div>
    <div class="content row flex-grow-1">
      <div id="menu" class="col-md-1 d-flex justify-content-start">
        <button v-on:click="onClickViewButton" class="btn btn-warning" style="cursor: pointer;">
          {{button_content}}
        </button>
      </div>
      <div v-show="isShow" id="input" class="col-xs-4 col-sm-5 col-md-5 col-lg-3">
        <div class="scroll-wrapper">
          <TripSelection
            v-on:googleQueryComplete="showGooglePrediction"
            v-on:tripComplete="showTripPrediction"
            :mode="mode"
          ></TripSelection>
        </div>
      </div>
      <div class="h-100 col-md-12">
        <Map></Map>
      </div>
    </div>
    
  </div>
</template>

<style lang="scss">
@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";

.dark-mode-toggle {
  /* 
    This will be no longer be in effect once the element is passed
    to the google map for rendering.
   */
  display: none;
}

:root {
  --container-color: #347AA0;
  --background-color: #E2E2E2;
  --border-color: #F3D463;
  --border-radius: 8px;
  --font-color: #000000;
  --counter-font-color: #ffffff;
}

#input {
  position: absolute;
  margin-top: 90px;
  margin-left: 40px;
  z-index: 2;
  background-color: var(--container-color);
  color: #F1ECED;
  border-radius: var(--border-radius);
  max-height: calc(100% - 300px);
  display: flex;
  flex-direction: column;
  justify-content: stretch;
  align-items: stretch;
}

.scroll-wrapper {
  overflow-y: auto;
  overflow-x: hidden;
  height: 100%;
}

#weather {
  z-index: 1;
}

.content.row {
  margin: 0 !important;
  padding: 0 !important;
}

.main {
  background-color: var(--container-color);
  text-align: center;
  height: 100vh;
  padding-bottom: 0.8em;
}

#menu {
  position: absolute;
  display: inline-block;
  z-index: 1;
  margin-top: 100px;
  
}

.bar {
  width: 35px;
  height: 5px;
  background-color: black;
  margin: 6px 0;
}

/* width */
::-webkit-scrollbar {
  width: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: var(--border-radius);
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: var(--border-radius);
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555;
}

@media only screen and (max-width: 992px) {

  #input {
    margin-left: 40px;
  }

  #weather {
    margin-left: 0%; 
  }

 }

@media only screen and (max-width: 600px) {

  .container-fluid {
    max-width: none;
    max-height: none;
  }
  
  #input {
    margin-top: 550px;
    margin-left: 0px;
    max-height: none;
  }

  #weather {
    position: absolute;
  }

  img {
    width: 50%;
  }

 }

/*
  A basic little spinning circle from W3C:
  https://www.w3schools.com/howto/howto_css_loader.asp
*/

.loader-template {
  border: 0.7em solid #f3f3f3; /* Light grey */
  border-top: 0.7em solid var(--border-color);
  border-radius: 50%;
  width: 5em;
  height: 5em;
  animation: loader-template-spin 2s linear infinite;
}

@keyframes loader-template-spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-warning{
  background-color: var(--border-color) !important;//overwrite the default color of bootstrap
}

</style>

<script>
/* eslint-disable no-undef */
import Map from "./components/Map";
import TripSelection from "./components/TripSelection"
import Weather from "./components/Weather"
import DarkMode from "@/components/DarkMode";

export default {
  name: "App",

  components: {
    DarkMode,
    Map,
    TripSelection,
    Weather,
  },

  data() {
    return {
      journeyInfo: '<b>Journey Info</b>',
      timestamp: null,
      selectedStop: null,
      isShow: true,
      button_content: '>',
      root: null,
      mode: 'light'
    };
  },

  methods:{
    onClickViewButton:function (){
      this.isShow = !this.isShow;
      this.button_content = this.button_content==='>'?'<':'>';
    },

    showTripPrediction:function (route, direction, stop_dep, stop_arr, timestamp){
      this.$refs.predict.getTripPrediction(route, direction, stop_dep, stop_arr, timestamp);
    },

    showGooglePrediction:function (route, timestamp){
      this.$refs.predict.getGooglePrediction(route, timestamp);
    },

    updateTimestamp:function (val){
      this.timestamp=val;
    },

    showStopTrips(stopID) {
      this.selectedStop = stopID;
    },

    changeMode: function (mode){
      if(mode ==='dark'){
        this.setDarkMode();
      }
      else {
        this.setLightMode();
      }
      this.mode=mode;
    },

    setLightMode: function (){
      this.root.style.setProperty('--background-color','#e2e2e2');
      this.root.style.setProperty('--font-color','#000000');
      this.root.style.setProperty('--counter-font-color','#ffffff');
      },

    setDarkMode: function (){
      this.root.style.setProperty('--background-color','#242f3e');
      this.root.style.setProperty('--font-color','#ffffff');
      this.root.style.setProperty('--counter-font-color','#000000');
    }
  },

  mounted() {
    this.root=document.documentElement
  }
}
</script>

