<template>
  <article>
      <header class="tabs">
        <ul ref="tab_list">
          <li v-for="(tab, index) in tabs" :key="index" class="col-3">
            <div class="nav-item"
                :class="{ 'is-active': tab.isActive }"
                @click="tabSelect(tab)">
              <img :src="tab.$attrs.img_link[mode]"/>
              <span class="nav-text">{{tab.name}}</span>
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
  .tabs {
    border: 2px solid var(--border-color);
    margin: 10px 10px;
    font-size: 1.0em;
    background-color: var(--background-color);
    border-radius: var(--border-radius);
  }

  .tabs-content {
    padding: 10px;
  }

  ul {
    margin: 0;
    display: flex;
    padding: 0;
    list-style: none;
    li {
      //margin-block: auto;
      //margin-right: 40px;
      // border-right: 2px solid #fefefe;
    }

    .nav-item .nav-text{
      visibility: hidden;
      width: 120px;
      background-color: black;
      color: #fff;
      text-align: center;
      border-radius: 6px;
      padding: 5px 0;
      position: absolute;
      z-index: 1;
    }

    .nav-item {
      cursor: pointer;
      color: var(--font-color);

      &:hover {
        background-color: var(--border-color);
        border-radius: var(--border-radius);
      }

      &:hover .nav-text{
        visibility: visible;
      }

      &.is-active {
        background-color: var(--border-color);
        border-radius: var(--border-radius);
      }
    }
  }
</style>