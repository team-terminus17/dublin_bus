<template>
  <div></div>
</template>

<script>
export default {
  name: "PointToPointRenderer",

  watch: {
    map: "refreshView"
  },

  data() {
    return {
      loading: false,
      stopsData: null,
      markers: [],
    };
  },

  computed: {
    map() {
      return this.$store.state.map
    }
  },

  created() {
    this.refreshView();
  },

  beforeDestroy() {
    this.removeMarkers();
  },

  methods: {
  }
};
</script>
