<template>
  <div id="app" style="padding:2em;text-align: start">
    <h1>{{time}}</h1>
    <time-picker v-model="time"></time-picker>
  </div>
</template>

<script lang="ts">


import { Component, Vue } from 'vue-property-decorator'
import TimePicker from '@/components/TimeInput.vue' // @ is an alias to /src
import ClockSelect from '@/components/ClockSelect.vue'

@Component({
  components: {
    TimePicker,
    ClockSelect
  },
})
export default class App extends Vue {
  time = "10:42"
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
</style>
