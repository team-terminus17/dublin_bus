<template>
  <div class="input-group">
    <input
        class="time-input form-control"
        type="text" maxlength="2" placeholder="HH"
        :value="internalValue.hours"
        @focusin="showClock('hours')"
        @input="updateValue($event.target.value, 'hours')"
        @focus="$event.target.select()"
    >
    <!--
      (Kieran) The styling below is inline so as to override the bootstrap default.
      Is there a better way of doing this?
    -->
    <span
        class="input-group-text"
        style="padding-left:0.1em;padding-right:0.1em"
    >
      :
    </span>
    <input
        class="time-input form-control"
        type="text" maxlength="2" placeholder="MM"
        :value="internalValue.minutes"
        @focusin="showClock('minutes')"
        @input="updateValue($event.target.value, 'minutes')"
        @focus="$event.target.select()"
    >
    <select
        class="form-select"
        @focusin="showClock(false)"
        @input="updateValue($event.target.value, 'suffix')"
    >
      <option selected>AM</option>
      <option>PM</option>
    </select>
    <button
        class="btn btn-outline-secondary dropdown-toggle.caret-off"
        ref="dropdown-toggle" data-bs-toggle="dropdown"
        type="button" data-bs-auto-close="outside" data-bs-reference="parent"
        style="display:none"
    >
      <img
          width="1em" height="1em"
          alt="show time selection"
          src="../assets/wall-clock.svg"
      >
    </button>
    <div ref="dropdown" class="dropdown-menu">
      <clock
          ref="clock"
          :kind="clockKind"
          :value="clockValue"
          @input="updateValue($event, clockKind)"
          @mouseup.native="nextClock"
      ></clock>
    </div>
  </div>
</template>

<style scoped lang="scss">

  $input-group-addon-padding-x: 0.1em;

</style>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */

import * as bootstrap from "bootstrap"
import Clock from "./TimeInputClock.vue"

export default {
  name: "TimeInput",
  components: {
    Clock
  },
  data() {
    return {
      clockKind: "hours"
    }
  },
  props: ["value"],
  computed: {
    internalValue,
    clockValue
  },
  methods: {
    showClock,
    nextClock,
    updateValue
  }
}

/*

  Computed properties

*/

function internalValue() {
  // Match HH:MM, or H:MM.
  // Allow for whitespace to either side, but nothing else.
  // Capture (HH?) and (MM)
  const pattern = /^\s*(\d?\d):(\d\d)\s*$/i

  const match = this.value.toString().match(pattern)
  if (!match)
    throw `Invalid value found for TimeInput: '${this.value}. Expected a time in HH:MM or H:MM format'`

  const value =  {
    hours: parseInt(match[1]),
    minutes: parseInt(match[2]),
    suffix: "none"
  }

  if (value.minutes < 0)
    value.minutes = 0
  else if (value.minutes > 59)
    value.minutes = 59

  if (value.hours < 0 || value.hours >= 24)
    value.hours = 0

  if (value.hours < 12)
    value.suffix = "AM"
  else {
    value.suffix = "PM"
    value.hours -= 12
  }

  if (value.hours === 0)
    value.hours = 12

  return value
}

function clockValue() {
  const value = this.internalValue
  if (this.clockKind === "hours")
    return value.hours
  else
    return value.minutes
}

/*

  Methods

*/

function showClock(kind) {
  if (kind) {
    const clock = this.$refs.clock
    if (!clock)
      return

    this.clockKind = kind
  }

  const toggle = this.$refs["dropdown-toggle"]
  if (!toggle)
    return

  const dropdown = new bootstrap.Dropdown(toggle, {
    autoClose: false
  })
  if (kind)
    dropdown.show()
  else
    dropdown.hide()
}

function nextClock() {
  if (this.clockKind === "hours")
    this.showClock("minutes")
  else
    this.showClock(false)
}

function updateValue(value, kind) {
  let { hours, minutes, suffix } = this.internalValue
  if (kind === "suffix")
    suffix = value
  else if (kind === "hours")
    hours = value
  else
    minutes = value

  if(hours === 12)
    hours = 0

  if (suffix === "PM")
    hours += 12

  hours = hours.toString()
  minutes = minutes.toString().padStart(2, "0")
  const newValue = hours + ":" + minutes

  // It seems to be bad practice to directly manipulate properties that
  // the parent has access to - the value given by the parent will take precedence.
  // The best we can do is kick the event up to the parent for it to deal with, say, with a v-model.
  this.$emit("input", newValue)
}

</script>
