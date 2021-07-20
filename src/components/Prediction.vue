<template>
  <div class="col-sm-12 col-md-12">
    <p>Journey Info:</p>
    <div>Time: {{ predict.time }}</div>
  </div>
</template>

<script>
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
      const predictionURL = "/predict/1/I/10/12/1624870800";
      const response = await fetch(predictionURL);
      const data = await response.json();
      console.log(data);

      this.predict.time = data.time;
    },
  },

  beforeMount() {
    this.getPrediction();
  },
};
</script>

<style>
</style>