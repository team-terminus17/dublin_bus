<template>
  <svg
    class="root" ref="root" height="10em" width="10em"
    viewBox="0 0 1 1"
    @mousedown="startDrag"
    @mousemove="continueDrag"
    @mouseup="stopDrag"
  >
    <clipPath :id="uuid + '-hand-clip'">
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
          class="number"
          v-for="item in clockFaceElements"
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
          :clip-path="'url(#' + uuid + '-hand-clip)'"
          class="active-number"
          v-for="item in clockFaceElements"
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

   /*
    The clock hand is moved by dragging, so it's best
    not to select the text with the same movement.
   */
  .root {
    user-select: none;
    background-color: var(--background-color);
  }

  /* The circle background */
  .face {
    fill: #dddddd;
  }

  /* Default color of the numbers 1-12 */
  .number {
    fill: black;
  }

  /* Color of the numbers 1-12, when highlighted */
  .active-number {
    fill: white;
  }

   /* Circle at the end of the clock hand */
  .hand {
    fill: var(--border-color);
  }

  /* Line from the center to the clock hand */
  .hand-line {
    stroke: var(--border-color);
    stroke-width: 0.025;
  }

</style>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */

class TextItem {
  x = 0
  y = 0
  text = ""
}

class Vector2 {
  x = 0
  y = 0
}

export default {
  name: "ClockSelect",
  data() {
    return {
      uuid: null,
      numberCount: 12,
      dragging: false,
      valueSet: false
    }
  },
  props: ["kind", "value"],
  created,
  computed: {
    internalKind,
    internalValue,
    step,
    useZero,
    numberBoxLength,
    radius,
    clockFaceElements,
    handPosition
  },
  methods: {
    startDrag,
    continueDrag,
    stopDrag,
    updateHandPosition
  }
}

/*

  Unique ID
  (For the sake of the clip-path attribute)

*/

let uuid = 0
function created() {
  this.uuid = uuid.toString()
  uuid += 1;
}

/*

  Computed properties

*/

function internalKind() {
  if (this.kind === "hours" || this.kind === "minutes")
    return this.kind
  throw `Clock select kind should be one of 'hours' or 'minutes', found '${this.kind}' instead`
}

function internalValue() {
  let result = parseInt(this.value.toString())
  if (isNaN(result))
    throw `Invalid value for clock select: '${this.value}'`
  return result
}

function step() {
  if (this.internalKind === "hours")
    return 1
  else
    // 12 numbers for 60 minutes or seconds
    return 5
}

function useZero() {
    return this.internalKind !== "hours"
}

function numberBoxLength() {
  const theta = 2*Math.PI/this.numberCount
  return Math.sqrt(1 - Math.cos(theta))
}

function radius() {
  return 1 - this.numberBoxLength/2
}

function clockFaceElements() {
  const result = []

  const radius = this.radius
  for (let n = 0; n < this.numberCount; n++) {

    const item = new TextItem()

    let theta = 2*n*Math.PI/this.numberCount
    theta -= Math.PI/2

    item.x = radius*Math.cos(theta)
    item.y = radius*Math.sin(theta)

    let itemText = n
    if (n === 0 && !this.useZero)
      itemText = this.numberCount
    item.text = (itemText*this.step).toString()

    result.push(item)

  }

  return result
}

function handPosition() {

  const p = this.internalValue / (this.numberCount*this.step)

  const theta = 2*Math.PI*p - Math.PI/2
  const radius = this.radius

  const result = new Vector2()
  result.x = radius*Math.cos(theta)
  result.y = radius*Math.sin(theta)

  return result

}

/*

  Methods

 */

function startDrag(event) {
  this.dragging = true
  this.updateHandPosition(event)
}

function stopDrag(event) {
  this.dragging = false
  this.updateHandPosition(event)
}

function continueDrag(event) {
  if (this.dragging)
    this.updateHandPosition(event)
}

function updateHandPosition(event) {

  // We can only update if the root is available

  const root = this.$refs.root
  if (!root)
    return

  // Calculate the hand angle

  let x = event.offsetX / root.clientWidth
  let y = event.offsetY / root.clientHeight

  x = 2*x - 1
  y = 2*y - 1

  let newAngle =  -Math.atan(x/y)
  if (isNaN(newAngle))
    newAngle = 0
  if (y >= 0)
    newAngle += Math.PI

  const step = 2*Math.PI/(this.numberCount*this.step)
  newAngle = step*(Math.round(newAngle/step))

  // From the hand angle, derive the value

  // This is silly, all that is needed is the angle mod 2pi, divided by 2pi
  // See: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Remainder
  const n = 2*Math.PI
  const p = (((newAngle % n) + n) % n)/(2*Math.PI)

  let newValue = this.step*this.numberCount*p
  newValue = Math.round(newValue)
  if (newValue === 0 && !this.useZero)
    newValue = this.numberCount*this.step

  // If the value has changed, emit an event.
  // Note that we are not changing any properties here! That's up to the parent element to bind/sync/model.

  if ((!this.valueSet) || newValue !== this.value) {
    this.$emit("update:value", newValue)
    this.$emit("input", newValue)
    this.valueSet = true
  }

}

</script>
