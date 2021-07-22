<template>
  <div id="map" style="width: 100%; height: 500px"></div>
</template>

<script>
import store from "@/store/index";
import bus from "./bus";

export default {
  name: "Map",
  store,

  created() {
    window.checkAndAttachMapScript(this.initMap);
  },

  methods: {
    initMap() {
      const map = new window.google.maps.Map(document.getElementById("map"), {
        center: { lat: 53.3673893, lng: -6.2600157 },
        zoom: 12,
      });

      this.$store.commit("initMap", map);

    },
  },
};
</script>
