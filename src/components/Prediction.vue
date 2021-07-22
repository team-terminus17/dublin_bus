<template>
  <div class="col-sm-12 col-md-3">
    <p>Journey Info:</p>
    <div>Time: {{ predict.time }}</div>
  </div>
</template>

<script>
import bus from "@/components/bus";
export default {
  data() {
    return {
      predict: {
        time: "test",
      },
    };
  },

  methods: {
    getPrediction: async function () {
      const predictionURL = '/predict/'+arguments[0]+'/'+arguments[1]+'/'+arguments[2]+'/'+arguments[3]+'/'+arguments[4]
      const response = await fetch(predictionURL);
      const data = await response.json();
      this.predict.time = data.time;
    },
  },

  beforeMount() {
    bus.$on("showPrediction",this.getPrediction)
  },
};
</script>

<style>
</style>