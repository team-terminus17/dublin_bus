<template>
  <div class="root">
    <header class="header">
      <button
          :class="{ visible: page > 0 }"
          @click="page--"
      >
        <i class="bi-caret-left-fill"></i>
      </button>
      <h1 class="title">{{title}}</h1>
      <button
          :class="{ visible: page < pageCount - 1 }"
          @click="page++"
      >
        <i class="bi-caret-right-fill"></i>
      </button>
    </header>
    <table class="table" @mouseup="setValueFromCell($event.target)">
      <tr>
        <th
            v-for="item in weekdays" :key="item"
            class="weekday"
        >
          {{item}}
        </th>
      </tr>
      <tr v-for="week in displayedWeeks" :key="week.id">
        <td
          v-for="day in week.days" :key="day.number"
          :class="{
            day: true,
            active: day.active,
            current: day.current,
            selected: day.selected
          }"
          :data-value="day.value"
          :data-active="day.active"
        >
          {{day.number}}
        </td>
      </tr>
    </table>
  </div>
</template>

<style scoped lang="scss">

.root {
  display: inline-block;
  padding: 0.3em;
  text-align: center;
  background-color: var(--background-color);
}

.header > button {
  border: none;
  box-shadow: none;
  background: none;
  color: grey;
  visibility: hidden;
}

.header > button.visible {
  visibility: visible;
}

.header > button:hover {
  color: black;
}

.title {
  font-size: 1em;
  margin: 0.2em;
  font-weight: bold;
  color: var(--font-color);
  display: inline-block;
}

.table {
  border-collapse: collapse;
  margin: 0;
}

.day, .weekday {
  padding: 0.2em;
  margin: 0.1em;
}

.weekday {
  font-weight: normal;
  color: var(--border-color);
}

.day {
  color: var(--counter-font-color);
}

.active {
    color: darkgray;
}

.day.active.current {
  color: var(--font-color);
}

.day.active.selected, .day.active.current.selected {
  background-color: var(--border-color);
  color: white;
  border-radius: 0.3em;
}

</style>

<script>
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */

import * as helper from "./DateInputHelpers"

const weekdays = [
    "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"
]

export default {
  name: "DateInputCalendar",
  data: function() {
    return {
      weekdays,
      page: 0
    }
  },
  props: ["startDate", "endDate", "value"],
  methods: {
    setValueFromCell
  },
  computed: {
    internalDateRange,
    internalValue,
    pageCount,
    title,
    displayedWeeks
  }
}

/*

  Methods

*/

function setValueFromCell(cell) {

  if (!cell.getAttribute("data-active"))
    return

  const value = cell.getAttribute("data-value")
  this.$emit("input", value)

}

/*

  Computed Properties

*/

function internalDateRange() {

  return helper.parseDateRange(this["startDate", this["endDate"]])

}

function internalValue() {

  let value = helper.parseISOString(this.value, "DateInputCalendar value")
  if (!value)
    value = new Date(Date.now())

  const range = this.internalDateRange

  if (value > range.end)
    value = range.end
  else if (value < range.start)
    value = range.start

  return value

}

function pageCount() {

  const range = this.internalDateRange
  const startMonths = range.start.getYear()*12 + range.start.getMonth()
  const endMonths = range.end.getYear()*12 + range.end.getMonth()
  return endMonths - startMonths + 1

}

function title() {

  let baseDate = new Date(this.internalDateRange.start)
  baseDate.setMonth(baseDate.getMonth() + this.page)

  const year = baseDate.toLocaleString('default', {'year':'numeric'})
  const month = baseDate.toLocaleString('default', {'month':'short'})
  return month + " " + year

}

function displayedWeeks() {

  const range = this.internalDateRange
  const value = this.internalValue

  const pageStart = new Date(range.start)
  pageStart.setMonth(pageStart.getMonth() + this.page)
  pageStart.setDate(1)

  const pageEnd = new Date(pageStart)
  pageEnd.setMonth(pageEnd.getMonth() + 1)
  pageEnd.setDate(pageEnd.getDate() - 1)

  if (pageStart.getMonth() === range.start.getMonth()
    && pageStart.getYear() === range.start.getYear()) {

    if (pageStart.getDate() < range.start.getDate())
      pageStart.setDate(range.start.getDate())

  }

  if (pageEnd.getMonth() === range.end.getMonth()
    && pageEnd.getYear() === range.end.getYear()) {

    if (pageEnd.getDate() > range.end.getDate())
      pageEnd.setDate(range.end.getDate())

  }

  const pageYear = pageStart.getYear()
  const pageMonth = pageStart.getMonth()

  const caret = new Date(pageStart)
  if (caret.getDay() === 0)
    caret.setDate(caret.getDate() - 1)
  caret.setDate(caret.getDate() - caret.getDay() + 1)

  const result = []

  let weekID = 0
  while(caret <= pageEnd) {

    const days = []
    for (let i = 0; i < 7; i++) {

      const active = caret >= range.start
        && caret <= range.end

      const current = caret.getMonth() === pageMonth
        && caret.getYear() === pageYear

      const selected = caret.getYear() === value.getYear()
        && caret.getMonth() === value.getMonth()
        && caret.getDate() === value.getDate()

      // The ISO, UTC, representation of the caret being used as the internal value
      // in this component.
      const caretInternalValue = helper.toISOString(caret)

      days.push({
        number: caret.getDate().toString().padStart(2, "0"),
        active, current, selected,
        value: caretInternalValue
      })

      caret.setDate(caret.getDate() + 1)

    }

    const week = {
      id: weekID,
      days
    }
    weekID++

    result.push(week)

  }

  return result

}

</script>