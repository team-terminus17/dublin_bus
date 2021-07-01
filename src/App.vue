<template>
  <div class="container" style="text-align: center; margin-top: 60px;">
      <div class="row">
        <div v-html="weather" class="col-sm-12 col-md-6 d-flex justify-content-start">
        
        </div>
        <div class="col-sm-12 col-md-6 d-flex justify-content-end">
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
import { ref, onMounted } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'

const GOOGLE_MAPS_API_KEY = 'AIzaSyDe8NaLRGPhWC8dppk014w_Mt6F_yNfI94'

export default {
  name: 'App',
  setup() {
      const loader = new Loader({ apiKey: GOOGLE_MAPS_API_KEY})
      const mapDiv = ref(null)
      onMounted(async () => {
        await loader.load()
        new google.maps.Map(mapDiv.value, {
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
      weather: '<b>Weather Info</b>',
      journeyInfo: '<b>Journey Info</b>',

      
    };
  }
}
</script>

<style>

</style>
