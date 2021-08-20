<template>
  <article class="tabs-container">
      <header class="tabs">
        <ul ref="tab_list">
          <li v-for="(tab, index) in tabs" :key="index" class="col-3">
            <div class="nav-item"
                :class="{ 'is-active': tab.isActive }"
                @click="tabSelect(tab)">
              <img class="tab-header-icon" :src="tab.$attrs.img_link[mode]"/>
            </div>
          </li>
        </ul>
      </header>
      <section class="tabs-content">
        <slot></slot>
      </section>
  </article>
</template>

<script>
export default {
  props:['mode'],

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
  .tabs-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .tabs {
    align-self: stretch;
    border: 2px solid var(--border-color);
    margin: 10px 10px;
    font-size: 1.0em;
    background-color: var(--background-color);
    border-radius: var(--border-radius);
  }
  
  ul {
    margin: 0;
    display: flex;
    padding: 0;
    list-style: none;
  }

  .tab-header-icon {
    max-height: 3em;
    max-width: 3em;
  }

  .tabs-content {
    padding: 10px;
    width: min(100vw, 25em);
    flex-grow: 1;
  }

  .nav-item {
    cursor: pointer;
    color: var(--font-color);
    height: 3em;
    display: flex;
    align-items: center;
    justify-content: center;
    align-content: center;

    &:hover {
      background-color: var(--border-color);
      border-radius: var(--border-radius);
    }

    &.is-active {
      background-color: var(--border-color);
      border-radius: var(--border-radius);
    }
  }
</style>