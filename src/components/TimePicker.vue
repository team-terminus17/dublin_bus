<template>
  <svg height="8.5em" width="8.5em">
    <rect width="100%" height="100%" style="fill:red"></rect>
      <rect
        v-for="shape in shapes"
        :key="shape.len"
        :x="shape.pos"
        :y="shape.pos"
        :width="shape.len"
        :height="shape.len"
        :style="shape.style"
    ></rect>
  </svg>
</template>

<script lang="ts">

import Vue from 'vue'
import Component from 'vue-class-component'

class Shape {
  pos: string
  len: string
  style: string
  constructor(pos: string, len: string, color: string) {
    this.pos = pos + "%";
    this.len = len + "%";
    this.style = "fill:" + color;
  }
}

@Component
export default class TimePicker extends Vue {
  get shapes(): Shape[] {
    return [
      new Shape("5", "90", "blue"),
      new Shape("10", "80", "yellow"),
      new Shape("15", "70", "red")
    ]
  }
}

</script>

<style scoped>

</style>