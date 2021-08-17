<template>
  <div>
    <input
      class="form-control"
      type="text" placeholder="YYYY-MM-DD"
      :value="inputText"
      @input="onTextInput($event.target.value)"
      @focusin="showCalendar(true)"
      @focus="$event.target.select()"
      @change="showCalendar(false)"
    >
    <button
        class="dropdown-toggle"
        ref="dropdown-toggle" data-bs-toggle="dropdown"
        style="display:none"
    ></button>
    <div ref="dropdown" class="dropdown-menu">
      <calendar
          v-model="internalValue"
          :start-date="startDate"
          :end-date="endDate"
          @input="showCalendar(false)"
      ></calendar>
    </div>
  </div>
</template>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */

import * as bootstrap from "bootstrap"
import Calendar from "./DateInputCalendar"
import * as helper from "./DateInputHelpers"
import { onClickaway, offClickaway } from "./clickaway.js"

export default {
  name: "DateInput",
  components: {
    Calendar
  },
  props: ["value", "startDate", "endDate"],
  data() {
    return {
      inputText: this.value,
      clickawayHandle: null,
      clickawayCount: 0,
    }
  },
  computed: {
    internalDateRange,
    internalValue: {
      get: getInternalValue,
      set: setInternalValue
    }
  },
  methods: {
    showCalendar,
    onTextInput
  }
}

/*

  Computed Properties

*/

function internalDateRange() {

  return helper.parseDateRange(this["startDate"], this["endDate"])

}

function getInternalValue() {

  const date = helper.parseISOString(this.value)

  if (!date)
    return helper.toISOString(new Date(Date.now()))

  // Yes, the text, not the date object.
  return this.value

}

function setInternalValue(newValue) {

  let date = helper.parseISOString(newValue)
  if (!date)
    date = helper.parseISOString(this.internalValue)

  const dateRange = this.internalDateRange
  if (date < dateRange.start)
    date = dateRange.start
  else if (date > dateRange.end)
    date = dateRange.end

  newValue = helper.toISOString(date)
  this.inputText = newValue

  this.$emit("input", newValue)

}

/*

  Methods

*/

function showCalendar(bool) {

  const toggle = this.$refs["dropdown-toggle"]
  if (!toggle)
    return

  const dropdown = new bootstrap.Dropdown(toggle, {
    autoClose: false,
    reference: "parent"
  })

  const calendar = this.$refs.dropdown

  if (bool) {
    dropdown.show()

    if (this.clickawayHandle) 
      offClickaway(this.clickawayHandle)

    // This is a bad workaround, but anyways. 
    // The clickaway event triggers once when the calendar is first shown,
    // which means that we actually want to dismiss the calendar on the second
    // instance of the event, which is what this count keeps track of.
    this.clickawayCount = 0

    this.clickawayHandle = onClickaway(calendar, () => {
      this.clickawayCount += 1
      if (this.clickawayCount > 1) {
        this.showCalendar(false);
      }
    })
  }
  else {
    if (this.clickawayHandle) 
      offClickaway(this.clickawayHandle)
      
    dropdown.hide()
  }

}

function onTextInput(newValue) {

  this.inputText = newValue

  const date = helper.parseISOString(newValue)
  if (date)
    this.internalValue = helper.toISOString(date)

}

</script>

<style scoped>

.form-control {
  color: var(--font-color);
  background-color: var(--background-color);
  border: 1px solid var(--border-color);
}

.dropdown-menu{
  background-color: var(--background-color);
}

</style>