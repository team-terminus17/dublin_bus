<template>
  <div id="color-mode" :class="mode">
    <div id="main">
      <DarkMode
        class="dark-mode-toggle"
        v-on:changeMode="changeMode"
      ></DarkMode>
      <ScrollButoon
        :mode="mode"
      ></ScrollButoon>
      <div id="view-content">
        <div class="row">
          <div class="col-sm-6 col-md-6 d-flex justify-content-start">
            <img id="logo" src="./assets/team.png" />
          </div>
          <div
            class="col-xs-6 col-sm-6 col-lg-6 d-flex justify-content-end"
            id="weather"
          >
            <Weather></Weather>
          </div>
        </div>
        <div class="row flex-grow-1">
          <div
            id="menu"
            class="d-none d-sm-grid col-md-1 d-flex justify-content-start"
          >
            <button
              v-on:click="onClickViewButton"
              class="btn btn-warning"
              style="cursor: pointer"
            >
              {{ button_content }}
            </button>
          </div>
          <div class="h-100 col-md-12">
            <Map></Map>
          </div>
        </div>
      </div>
      <div
        v-show="isShow"
        id="input-content"
      >
        <div class="scroll-wrapper">
          <TripSelection
            v-on:googleQueryComplete="showGooglePrediction"
            v-on:tripComplete="showTripPrediction"
            :mode="mode"
          ></TripSelection>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";

/* 
  Colors and Theming
*/

.dark-mode-toggle {
  /* 
    This will be no longer be in effect once the element is passed
    to the google map for rendering.
   */
  display: none;
}

:root {
  --border-radius: 8px;
}

#color-mode.light * {
  --container-color: #347aa0;
  --main-border-color: #347aa0;
  --background-color: #e2e2e2;
  --border-color: #f3d463;
  --font-color: #000000;
  --counter-font-color: #7a7a7a;
}

#color-mode.dark * {
  --main-border-color: #17263c;
  --container-color: #2e4a7a;
  --background-color: #242f3e;
  --border-color: #d59563;
  --font-color: #ffffff;
  --counter-font-color: #000000;
}

/*
  Main page layout
  (Also includes some input styling)
*/

#main {
  background-color: var(--main-border-color);
  text-align: center;
  padding-bottom: 0.8em;
  height: 100vh;
}

#view-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

#view-content > .row {
  margin: 0 !important;
  padding: 0 !important;
}

#input-content {
  position: absolute;
  top: 11em;
  left: 4em;
  max-height: calc(100% - 16em);
  max-width: 25em;
  z-index: 2;
  background-color: var(--container-color);
  color: #f1eced;
  border-radius: var(--border-radius);
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

#menu {
  position: absolute;
  display: inline-block;
  z-index: 1;
  margin-top: 100px;
}

@media only screen and (max-width: 992px) {
  #input-content {
    left: 3em;
  }

  #weather {
    margin-left: 0%;
  }

  #view-content {
    /* 
      Leave space for the tab buttons down below. 
      This is sensitive to the spacing defined on the tab buttons!
    */
    height: calc(100vh - 4.5em)
  }

  #input-content {
    position: static;
    max-height: none;
    max-width: none;
  }
}

@media only screen and (max-width: 600px) {
  #weather {
    position: absolute;
  }

  img {
    width: 50%;
  }
}

/*
  Scrollbar Styling
  Currently Chrome only.
*/

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: var(--border-radius);
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: var(--border-radius);
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/*
  Loading symbol template
  From: https://www.w3schools.com/howto/howto_css_loader.asp
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
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.btn-warning {
  background-color: var(
    --border-color
  ) !important; //overwrite the default color of bootstrap
  border-color: var(--border-color) !important;
}
</style>

<script>
/* eslint-disable no-undef */
import Map from "./components/Map";
import TripSelection from "./components/TripSelection";
import Weather from "./components/Weather";
import DarkMode from "@/components/DarkMode";
import ScrollButoon from "@/components/ScrollButoon";

export default {
  name: "App",

  components: {
    ScrollButoon,
    DarkMode,
    Map,
    TripSelection,
    Weather,
  },

  data() {
    return {
      journeyInfo: "<b>Journey Info</b>",
      timestamp: null,
      selectedStop: null,
      isShow: true,
      button_content: ">",
      root: null,
      mode: "light",
    };
  },

  methods: {
    onClickViewButton: function () {
      this.isShow = !this.isShow;
      this.button_content = this.button_content === ">" ? "<" : ">";
    },

    showTripPrediction: function (
      route,
      direction,
      stop_dep,
      stop_arr,
      timestamp
    ) {
      this.$refs.predict.getTripPrediction(
        route,
        direction,
        stop_dep,
        stop_arr,
        timestamp
      );
    },

    showGooglePrediction: function (route, timestamp) {
      this.$refs.predict.getGooglePrediction(route, timestamp);
    },

    updateTimestamp: function (val) {
      this.timestamp = val;
    },

    showStopTrips(stopID) {
      this.selectedStop = stopID;
    },

    changeMode: function (mode) {
      this.mode = mode;
    },
  },

  mounted() {
    this.root = document.documentElement;
  },
};
</script>

