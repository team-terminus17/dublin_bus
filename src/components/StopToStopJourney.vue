<template>
  <div>
    <div v-html="journey" class="d-flex"></div>
    <div
      class="col-md-4 justify-content-space-between"
      style="margin-top: 20px"
    >
      <label class="d-flex justify-content-start">Route Selection</label>
      <RouteSelection v-on:selectRoute="getRoute"></RouteSelection>
    </div>
    <div class="col-md-12">
      <div class="form-group" style="margin-top: 6px">
        <label class="d-flex justify-content-start">Start Stop</label>
        <StopSelection v-on:stopSelected="getDepStop"></StopSelection>
      </div>
      <div class="form-group" style="margin-top: 10px">
        <label class="d-flex justify-content-start">End Stop</label>
        <StopSelection v-on:stopSelected="getArrStop"></StopSelection>
      </div>
    </div>
    <div class="col-md-12" style="margin-top: 10px">
      <DateTimeInput></DateTimeInput>
    </div>
    <button
      @click="handle"
      type="button"
      class="btn btn-warning"
      style="margin-top: 70px"
    >
      Submit
    </button>
  </div>
</template>

<script>
import DateTimeInput from "./DateTimeInput.vue";
import RouteSelection from "@/components/RouteSelection";
import StopSelection from "@/components/StopSelection";
export default {
  components: { DateTimeInput, RouteSelection, StopSelection },
};
</script>

<style>
</style>