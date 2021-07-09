<template>
  <div>
    <div class="row">
        <div v-html="journey" class="d-flex justify-content-start"></div>
    </div>
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
  </div>
</template>

<script>

import Vue from "vue"
import Component from "vue-class-component"

@Component
export default class TripSelection extends Vue {

  journey = "Please input your journey info:"

}

</script>

<style scoped>

</style>