<template>
  <div id="app" style="padding:2em;text-align: start">
    <div class="time">
      <h1>{{time}}</h1>
      <time-picker style="width:11em;" v-model="time"></time-picker>
    </div>
    <div class="date">
      <h1>{{date}}</h1>
      <date-picker
          style="width:11em;display:inline-block"
          v-model="date"
          start-date="2021-07-08"
          end-date="2021-07-19"
      ></date-picker>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator'
import TimePicker from '@/components/TimeInput.vue' // @ is an alias to /src
import Clock from '@/components/TimeInputClock.vue'
import DatePicker from "@/components/DateInput.vue"
import Calendar from "@/components/DateInputCalendar.vue"

@Component({
  components: {
    TimePicker,
    Clock,
    DatePicker,
    Calendar
  },
})
export default class App extends Vue {
  time = "10:42"
  date = "2021-07-08"
}

</script>

<style lang="scss">

@import "../node_modules/bootstrap-icons/font/bootstrap-icons.css";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}

h1 {
  padding: 0.5em;
}

.time, .date {
  display: inline-block;
  padding: 0 2em;
  text-align: center;
}

</style>
