<template>
  <div class="input-group" style="width: 14.5em">
    <input
        class="time-input form-control"
        type="text" maxlength="2" placeholder="HH" value="14"
        v-model.number="hours"
        @focusin="showClock('hours')"
        @change="updateClock"
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
        type="text" maxlength="2" placeholder="MM" value="00"
        v-model.number="minutes"
        @focusin="showClock('minutes')"
    >
    <select class="form-select" @focusin="showClock(false)">
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
      <clock-select
          ref="clock" :kind="clockKind"
          v-model="clockValue"
          @input="updateFromClock"
          @mouseup.native="nextClock"
      ></clock-select>
    </div>
  </div>
</template>

<style scoped lang="scss">

  $input-group-addon-padding-x: 0.1em;

</style>

<script>

import Vue from "vue"
import * as bootstrap from "bootstrap"
import ClockSelect from "@/components/ClockSelect.vue"

export default Vue.extend({
  name: "TimeInput",
  data: function() {
    return {
      hours: 5,
      minutes: 15,
      clockKind: "hours",
      clockValue: 1
    }
  },
  components: {
    ClockSelect
  },
  methods: {
    showClock(kind) {

      if (kind) {
        const clock = this.$refs.clock
        if (!clock)
          return
        this.clockKind = kind
        clock.kind = kind
        if (kind === "hours")
          this.clockValue = this.hours
        else
          this.clockValue = this.minutes
        clock.value = this.clockValue
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

    },
    updateClock() {
      if (this.clockKind === "hours")
        this.clockValue = this.hours
      else
        this.clockValue = this.minutes
    },
    updateFromClock() {
      if (this.clockKind === "hours")
        this.hours = this.clockValue
      else
        this.minutes = this.clockValue
    },
    nextClock() {
      if (this.clockKind === "hours")
        this.showClock("minutes")
      else
        this.showClock(false)
    }
  }
})

</script>
