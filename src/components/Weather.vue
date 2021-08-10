<template>
      <div class="temp">
        <span>{{ weather.temp }}&deg;C</span>
        <!-- <p class="my-4">Rain: {{ weather.description }}</p> -->
        <span v-html="weather.icon"></span>
      </div>
</template>

<script>
export default {
  data() {
    return {
      weather: {
        temp: 14,
        description: "null",
        icon: "10n",
      },
    };
  },

  methods: {
    getWeather: async function () {
      const weatherURL = "/weather";

      const response = await fetch(weatherURL);
      const data = await response.json();
      console.log(data);
      this.weather.temp = Math.round(data.temp);
      this.weather.description = data.rain;
      this.weather.icon = "<img src=\"http://openweathermap.org/img/wn/" + data.icon + "@2x.png\"></img>";
    },
  },

  beforeMount() {
    this.getWeather();
  },
};
</script>

<style scoped>

.temp {
  font-weight: 100;
  font-size: 1.5em;
  letter-spacing: -1px;
  white-space: nowrap;
  color: white;
}

.card-mid {
line-height: 0.1;
}

@media only screen and (max-width: 992px) {


}

@media only screen and (max-width: 600px) {

  .temp {
    width: 50%;
    font-size: 1.2em;
  }

}
</style>