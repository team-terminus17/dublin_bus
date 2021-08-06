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
  width: 100%;
  height: 900px;
  border-radius: 10px;
  margin-top: 0px;
}

@media only screen and (max-width: 992px) {
  #map {
  margin-top: 0px;
  height: 950px;
  }

}

@media only screen and (max-width: 600px) {
  #map {
    /* margin-top: -120px; */
    height: 550px;
  }
}

</style>