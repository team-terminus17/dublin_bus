<template>
  <div class="container" style="text-align: center; margin-top: 60px;">
      <div class="row">
        <div class="col-sm-12 col-md-4 d-flex justify-content-start card rounded my-3 shadow-lg back-card overflow-hidden">
         
        

        <!--card middle body, card body used cos I want to just update the innerHTML -->
        <div class="card-body">
          <!-- card middle starts here -->
          <div class="card-mid">
            <div class="row">
              <div class="col-md-4 text-center temp">
                <span>{{weather.temp}}&deg;C</span>
                <p class="my-4">Rain:{{weather.description}}</p>
              </div>
              <div class="col-md-4">
                <span>{{weather.icon}}</span>
              </div>
              <div class="col-md-4">
                <p>{{weather.cityName}}</p>
                <p class="">{{weather.country}}</p>
              </div>
            </div>
            
          </div>
          <!-- card middle ends here -->

        </div>
      </div>
      <div class="col-sm-12 col-md-8 d-flex justify-content-end">
        <button type="button" class="btn btn-light">Light</button>
        <button type="button" class="btn btn-dark">Dark</button>
      </div>
    </div>
    <Map></Map>
    <TripSelection></TripSelection>
    <div class="row" style="margin-top: 20px;">
      <div class="col-sm-12 col-md-3">
        <p>Journey Info:</p>
        <div>
          Time: {{predict.time}}
        </div>
      </div>
    </div>
  </div> 
</template>

<script>
/* eslint-disable no-undef */
import Map from "./components/Map";
import TripSelection from "./components/TripSelection"
export default {
  name: 'App',
  components: {
    Map,
    TripSelection
  },
  data() {
    return {
      greet: 'Hello there',
      name: "General Kenobi",
      headingID: 'heading',
      isDisabled: false,
      status: 'success',
      journeyInfo: '<b>Journey Info</b>',
      weather:{
        cityName:"Dublin",
        country:"Ireland",
        temp: 12,
        description:"Clouds up in this",
        lowTemp:"19",
        highTemp:"27",
        feelsLike:"20",
        humidity:"55",
        icon: 10n,
      },

      predict:{
        time: "test",
      },

    };
  },
  methods: {
    getWeather: async function () {
      // const key = "078742f65d44394818f07213310b1fca"
      // const baseURL = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&appid='+ key +'&units=metric'
      const weatherURL = '/weather'
      

      const response = await fetch(weatherURL)
      const data = await response.json()
      // console.log(data);

      // this.weather.cityName = data.name;
      // this.weather.country = data.sys.country;
      this.weather.temp = Math.round(data.temp);
      this.weather.description = data.rain;
      // this.weather.lowTemp = Math.round(data.main.temp_min);
      // this.weather.highTemp = Math.round(data.main.temp_max);
      // this.weather.feelsLike = Math.round(data.main.feels_like);
      // this.weather.humidity = Math.round(data.main.humidity);
      this.weather.icon = data.icon;

      // const iconURL = './assets/openweathermap-api-icons-master/icons/'+ data.icon +'.png'
      // this.weather.icon = await fetch(iconURL)
      // console.log(this.weather.icon)
    },

    getPrediction: async function () {
      const predictionURL = '/predict/1/I/10/12/1624870800'

      const response = await fetch(predictionURL)
      const data = await response.json()
      console.log(data);

      this.predict.time = data.time;
    }
  },

  beforeMount(){
    this.getWeather()
    this.getPrediction()
  },
}
</script>

<style>
@import "./assets/custom.css";
</style>
