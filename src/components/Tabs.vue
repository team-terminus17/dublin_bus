<template>
  <article>
      <header class="tabs">
        <ul>
          <li v-for="(tab, index) in tabs" :key="index">
            <div class="nav-item"
                :class="{ 'is-active': tab.isActive }"
                @click="tabSelect(tab)">
              {{ tab.name}}
            </div>
          </li>
        </ul>
      </header>
      <section class="tabs-content">
        <slot>

        </slot>
      </section>
  </article>
</template>

<script>
export default {
  data: () => {
    return {
      tabs: []
    }
  },

  methods: {
    tabSelect(selectedTab) {
      this.tabs.forEach(tab => {
        let prevstate = tab.isActive
        tab.isActive = tab.name === selectedTab.name;
        if(prevstate==false && tab.isActive==true){
          this.$emit("tabChanged")
        }
      });
    }
  },

  created() {
    this.tabs = this.$children;
  }
};
</script>

<style lang="scss" scoped>
  .tabs {
    border: 2px solid var(--border-color);
    margin: 0 10px;
    margin-top: 10px;
    font-size: 1.0em;
    background-color: var(--background-color);
    border-radius: var(--border-radius);
    overflow-x: hidden;
  }

  .tabs-content {
    padding: 10px;
  }

  ul {
    display: flex;
    padding: 0;
    list-style: none;
    
    li {
      margin-right: 40px;
      // border-right: 2px solid #fefefe;
    }

    .nav-item {
      cursor: pointer;
      color: black;

      &:hover {
        background-color: var(--border-color);
        border-radius: var(--border-radius);
      }

      &.is-active {
        background-color: var(--border-color);
        border-radius: var(--border-radius);
      }
    }
  }
</style>