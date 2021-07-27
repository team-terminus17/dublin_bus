<template>
    <div
      class="
        col-xs-2
        col-sm-2
        col-md-1
        
        
        overflow-hidden
      "
      id="weather"
    >
      <div class="card-body">
        <div class="card-mid">
          <div class="row">
            <div class="col-sm-6 col-md-4 temp">
              <span>{{ weather.temp }}&deg;C</span>
              <!-- <p class="my-4">Rain: {{ weather.description }}</p> -->
            </div>
            <div class="col-sm-6 col-md-8">
              <span v-html="weather.icon"></span>
            </div>
          </div>
        </div>
      </div>
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

#weather {
  z-index: 1;
}

/* .back-card {
border-radius: 40px !important;
color: white;
background: linear-gradient(to bottom right, #707070, #434647);
text-shadow: 2px 2px 2px #707070;
} */

.temp {
font-weight: 100;
font-size: 1.5em;
letter-spacing: -1px;
white-space: nowrap;
margin-top: 30%;
}

.card-body {
  margin-bottom: -30px;
}

.card-mid {
line-height: 0.1;
}
</style>