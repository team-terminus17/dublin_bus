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
        tab.isActive = tab.name === selectedTab.name;
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
    border-bottom: 2px solid #fefefe;
    margin: 0 10px;
    margin-top: 10px;
    font-size: 1.2em;
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
    }

    .nav-item {
      cursor: pointer;

      &:hover {
        color: #bbdaa4;
      }

      &.is-active {
        color: #bbdaa4;
      }
    }
  }
</style>