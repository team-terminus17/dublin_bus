<template>
  <div>
    <!--
      It's an ongoing debate is to whether this label should be here,
      hence the comment.
      <label class="d-flex justify-content-start">Date & Time</label>
    -->
    <div class="date" :style="`margin-bottom: ${gap}`">
      <DateInput v-model="date"></DateInput>
    </div>
    <div>
      <TimeInput v-model="time"></TimeInput>
    </div>
  </div>
</template>

<script>
import TimeInput from "@/components/TimeInput";
import DateInput from "@/components/DateInput";
export default {
  name: "DateTimeInput",

  components: {
    TimeInput,
    DateInput,
  },

  props: ["gap"],

  data() {
    return {
      date: null,
      time: null,
      timestamp: null,
    };
  },

  methods: {
    initDateTime: function () {
      function getTwoDigit(num) {
        return (num < 10 ? "0" : "") + num;
      }
      let dt = new Date();
      let Y = dt.getFullYear();
      let MO = getTwoDigit(dt.getMonth() + 1);
      let D = getTwoDigit(dt.getDate());
      let H = getTwoDigit(dt.getHours());
      let MI = getTwoDigit(dt.getMinutes());
      this.date = Y + "-" + MO + "-" + D;
      this.time = H + ":" + MI;
    },

    changeTimestamp: function () {
      this.timestamp = Date.parse(this.date + " " + this.time) / 1000;
    },
  },

  watch: {
    time(newtime, oldtime) {
      if (oldtime != newtime) {
        this.changeTimestamp();
      }
    },

    date(newdate, olddate) {
      if (newdate != olddate) {
        this.changeTimestamp();
      }
    },

    timestamp(newval, oldval) {
      if (oldval != newval) {
        this.$emit("sendTimestamp", this.timestamp);
      }
    },
  },

  created() {
    this.initDateTime();
  },
};
</script>
