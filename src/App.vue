<template>
  <div id="app">
    <time-picker></time-picker>
  </div>
</template>

<script lang="ts">


import { Component, Vue } from 'vue-property-decorator';
import TimePicker from '@/components/ClockSelect.vue'; // @ is an alias to /src

@Component({
  components: {
    TimePicker,
  },
})
export default class App extends Vue {}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
</style>
