<template>
    <div id="map">
    </div>
</template>

<script>
import store from "@/store/index";

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

<style scoped>

#map {
  height: 100%;
  width: 100%;
  border-radius: 10px;
  margin-top: 0px;
}

</style>