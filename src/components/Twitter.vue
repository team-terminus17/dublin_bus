<template>
  <div>
    <Timeline
      id="dublinbusnews"
      sourceType="profile"
      widget-class="twitter"
      :options="{theme: mode}"
      :key="mode"
    />
  </div>
</template>

<script>
import { Timeline } from "vue-tweet-embed";

export default {
  name: "Twitter",
  components: {
    Timeline,
  },
  props: ["mode"],
};
</script>

<style scoped>
.twitter {
  margin: 2em 0;
}
</style>