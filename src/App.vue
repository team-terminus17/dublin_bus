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
    <div class="row">
      {{greet}} {{name}}
    </div>
    <div class="row" ref="mapDiv" style="width: 100%; height: 500px">
    </div>
    
    <div class="row">
        <div v-html="journey" class="d-flex justify-content-start"></div>
    </div>
    <div class="row" style="margin-top: 20px;">
      <div class="col-sm-3 col-md-2" style="margin-top: 30px;">
        <div class="btn-group">
          <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            Bus Route

          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">9</a></li>
            <li><a class="dropdown-item" href="#">46a</a></li>
            <li><a class="dropdown-item" href="#">145</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Separated link</a></li>
          </ul>
        </div>
      </div>
      <div class="col-sm-3 col-md-2">
        <form>
          <div class="form-group" style="margin-top: 6px;">
            <label for="originStop" class="d-flex justify-content-start">Origin Stop</label>
            <input type="origin" class="form-control" id="originStop" placeholder="Enter origin stop">
          </div>
          <div class="form-group" style="margin-top: 6px;">
            <label for="destinationStop" class="d-flex justify-content-start">Destination Stop</label>
            <input type="destination" class="form-control" id="destinationStop" placeholder="Enter destination stop">
          </div>
        </form>
      </div>
      <div class="col-sm-4 col-md-3">
        <div class="btn-group" style="margin-top: 30px;">
          <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            Day of the Week

          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Monday</a></li>
            <li><a class="dropdown-item" href="#">Tuesday</a></li>
            <li><a class="dropdown-item" href="#">Wednesday</a></li>
            <li><a class="dropdown-item" href="#">Thursday</a></li>
            <li><a class="dropdown-item" href="#">Friday</a></li>
            <li><a class="dropdown-item" href="#">Saturday</a></li>
            <li><a class="dropdown-item" href="#">Sunday</a></li>
          </ul>
          
        </div>
        <div class="btn-group" style="margin-top: 30px;">
          <button type="button" class="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
            Departure time

          </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">9</a></li>
            <li><a class="dropdown-item" href="#">46a</a></li>
            <li><a class="dropdown-item" href="#">145</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Separated link</a></li>
          </ul>
        </div>
      </div>
      <div class="col-sm-2 col-md-2">
        <button type="button" class="btn btn-warning" style="margin-top: 70px;">Submit</button>
      </div>
      <div class="col-sm-12 col-md-3">
        <div v-html="journeyInfo" >
        
        </div>
      </div>
    </div>
  </div> 
</template>

<script>
/* eslint-disable no-undef */
// import { ref, mounted } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'

const GOOGLE_MAPS_API_KEY = 'AIzaSyDe8NaLRGPhWC8dppk014w_Mt6F_yNfI94'

export default {
  name: 'App',
  setup() {
      const loader = new Loader({ apiKey: GOOGLE_MAPS_API_KEY})
      const mapDiv = this.$refs.null
      mounted(async () => {
        await loader.load()
        new google.maps.Map(this.$refs.mapDiv.value, {
          center: {lat: 53.3673893, lng: -6.2600157},
          zoom: 12
        })
      })
      return { mapDiv }
    },
  
  data() {
    return {
      greet: 'Hello there',
      name: "General Kenobi",
      journey: '<b>Please input your journey info:</b>',
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

      
    };
  },
  methods: {
    getWeather: async function () {
      // const key = "078742f65d44394818f07213310b1fca"
      // const baseURL = 'http://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&appid='+ key +'&units=metric'
      const weatherURL = '/weather'
      

      const response = await fetch(weatherURL)
      const data = await response.json()
      console.log(data);

      // this.weather.cityName = data.name;
      // this.weather.country = data.sys.country;
      this.weather.temp = Math.round(data.temp);
      this.weather.description = data.rain;
      // this.weather.lowTemp = Math.round(data.main.temp_min);
      // this.weather.highTemp = Math.round(data.main.temp_max);
      // this.weather.feelsLike = Math.round(data.main.feels_like);
      // this.weather.humidity = Math.round(data.main.humidity);
      // this.weather.icon = data.icon;

      const iconURL = './assets/openweathermap-api-icons-master/icons/'+ data.icon +'.png'
      this.weather.icon = fetch(iconURL)
    }
  },

  beforeMount(){
    this.getWeather()
  },
}
</script>

<style>
@import "./assets/custom.css";
</style>
