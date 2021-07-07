<template>
  <svg
    id="root" ref="root" height="10em" width="10em"
    viewBox="0 0 1 1"
    @mousedown="startDrag"
    @mousemove="continueDrag"
    @mouseup="stopDrag"
  >
    <clipPath id="hand-clip">
      <circle
        :r="numberBoxLength/2"
        :cx="handPosition.x"
        :cy="handPosition.y"
      ></circle>
    </clipPath>
    <circle
      class="face"
      cx="0.5"
      cy="0.5"
      r="0.5"
    ></circle>
    <g transform="translate(0.5 0.5) scale(0.5)">
      <circle
        class="hand"
        r="0.05"
      ></circle>
      <line
        class="hand-line"
        x1="0" y1="0"
        :x2="handPosition.x"
        :y2="handPosition.y"
      ></line>
      <text
          :id="item.text"
          class="number"
          v-for="item in numberItems"
          :key="item.text"
          :x="item.x"
          :y="item.y"
          text-anchor="middle"
          dominant-baseline="central"
          :font-size="numberBoxLength/2"
      >
        {{item.text}}
      </text>
      <circle
        class="hand"
        :r="numberBoxLength/2"
        :cx="handPosition.x"
        :cy="handPosition.y"
      ></circle>
      <text
          clip-path="url(#hand-clip)"
          :id="item.text + ' (active)'"
          class="active-number"
          v-for="item in numberItems"
          :key="item.text + ' (active)'"
          :x="item.x"
          :y="item.y"
          text-anchor="middle"
          dominant-baseline="central"
          :font-size="numberBoxLength/2"
      >
        {{item.text}}
      </text>
    </g>
  </svg>
</template>

<style scoped>

  #root {
    user-select: none;
  }

  .face {
    fill: #dddddd;
  }

  .number {
    fill: black;
  }

  .active-number {
    fill: white;
  }

  .hand {
    fill: dodgerblue;
  }

  .hand-line {
    stroke: dodgerblue;
    stroke-width: 0.025;
  }

</style>

<script lang="ts">

import { Vue, Component, Prop } from "vue-property-decorator"

class TextItem {
  x = 0
  y = 0
  text = ""
}

class Vector2 {
  x = 0
  y = 0
}

@Component
export default class ClockSelect extends Vue {

  // Data

  numberCount = 12
  selectionAngle = 0

  dragging = false
  valueSet = false

  // Properties

  @Prop({
    type: String,
    default: "hours"
  })
  kind!: "hours" | "minutes" | "seconds"

  // Computer Properties

  get scale(): number {
    if (this.kind === "hours")
      return 1
    else
      // 12 numbers for 60 minutes or seconds
      return 5
  }

  get useZero(): boolean {
      return this.kind !== "hours"
  }

  get numberBoxLength(): number {
    const theta = 2*Math.PI/this.numberCount
    return Math.sqrt(1 - Math.cos(theta))
  }

  get radius(): number {
    return 1 - this.numberBoxLength/2
  }

  get numberItems(): TextItem[] {
    const result = []

    const radius = this.radius
    for (let n = 0; n < this.numberCount; n++) {

      const item = new TextItem()

      let theta = 2*n*Math.PI/this.numberCount
      theta -= Math.PI/2

      item.x = radius*Math.cos(theta)
      item.y = radius*Math.sin(theta)

      let itemText = n
      if (n == 0 && !this.useZero)
        itemText = this.numberCount
      item.text = (itemText*this.scale).toString()

      result.push(item)

    }

    return result
  }

  get handPosition(): Vector2 {

    const theta = this.selectionAngle - Math.PI/2
    const radius = this.radius

    const result = new Vector2()
    result.x = radius*Math.cos(theta)
    result.y = radius*Math.sin(theta)

    return result

  }

  get value(): number {

    const a = this.selectionAngle
    const n = 2*Math.PI

    // This is silly, all I want is the angle mod 2pi, divided by 2pi
    // See: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Remainder
    const p = (((a % n) + n) % n)/(2*Math.PI)

    let result = this.scale*this.numberCount*p
    result = Math.round(result)
    if (result === 0 && !this.useZero)
      result = this.numberCount*this.scale

    return result

  }

  set value(newValue: number) {

    const maxValue = this.scale*this.numberCount
    newValue = Math.max(0, Math.min(newValue, maxValue))
    this.selectionAngle = 2*Math.PI*(newValue/maxValue)

  }

  // Methods

  startDrag(event: MouseEvent): void {
    this.dragging = true
    this.updateHandPosition(event)
  }

  stopDrag(event: MouseEvent): void {
    this.dragging = false
    this.updateHandPosition(event)
  }

  continueDrag(event: MouseEvent): void {
    if (this.dragging)
      this.updateHandPosition(event)
  }

  updateHandPosition(event: MouseEvent): void {

    const root = this.$refs.root as Element
    if (!root)
      return

    let x = event.offsetX / root.clientWidth
    let y = event.offsetY / root.clientHeight

    x = 2*x - 1
    y = 2*y - 1

    let newAngle =  -Math.atan(x/y)
    if (y >= 0)
      newAngle += Math.PI

    const step = 2*Math.PI/(this.numberCount*this.scale)
    newAngle = step*(Math.round(newAngle/step))

    if ((!this.valueSet) || newAngle !== this.selectionAngle) {
      this.selectionAngle = newAngle
      this.$emit("input", this.value)
      this.valueSet = true
    }

  }

}

</script>
