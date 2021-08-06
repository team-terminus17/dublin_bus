<template>
    <div
      class="
        col-sm-2
        col-md-3
        col-lg-3
        overflow-hidden
      "
      id="weather"
    >
      <div class="card-body temp">
        <span id="back">{{ weather.temp }}&deg;C</span>
        <!-- <p class="my-4">Rain: {{ weather.description }}</p> -->
        <span id="back" v-html="weather.icon"></span>
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
  position: absolute;
  margin-left: 75%;
  margin-top: -35px;
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
  margin-bottom: -40px;
  color: white;
}

/* #back {
  background-color: #6e99f5;
  border-radius: 8px;
  
} */

.card-mid {
line-height: 0.1;
}

@media only screen and (max-width: 992px) {


}

@media only screen and (max-width: 600px) {
  
  #weather {
    margin-left: 0%;
    
  }

  .temp {
    width: 50%;
  }

}
</style>