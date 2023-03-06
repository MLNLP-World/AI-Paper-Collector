<!--
 * @Author: 0x3E5
 * @Date: 2023-02-12 17:29:45
 * @LastEditTime: 2023-03-06 10:34:09
 * @LastEditors: 0x3E5
 * @Description: 
 * @FilePath: \web-vue\src\components\ConfsTree.vue
-->
<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
const props = defineProps(['data'])
const emits = defineEmits<{
  (e: 'click', val: Object): void
}>()

interface Tree {
  label: string
  children?: Tree[]
}

const total = ref(0)
const tree = reactive({
  val: [
    {
      label: `All (0)`,
      children: []
    }
  ]
})

const defaultProps = {
  children: 'children',
  label: 'label'
}

const formatData: (treeData: Object, target: Tree) => void = (
  treeData,
  target
) => {
  if (Array.isArray(treeData)) {
    // level1 total
    total.value += treeData.length
    tree.val[0].label = `All (${total.value})`
    // level3 total
    target.label = `${target.label} (${treeData.length})`
    return treeData.length
  } else {
    // level2 total
    let level2Total = ref(0)
    for (let k in treeData) {
      let itm = { label: k, children: [] }
      target.children?.push(itm)
      level2Total.value += Number(formatData((treeData as any)[k], itm)) || 0
    }
    if (!target.label.startsWith('All')) {
      target.label = `${target.label} (${level2Total.value})`
    }
  }
}

const treeNodeClick = (objData: Tree, node: any) => {
  if (node.level === 3) {
    emits('click', {
      level: node.level,
      key: node.data.label.split(' ')[0],
      parent: node.parent.data.label.split(' ')[0]
    })
  } else {
    emits('click', { level: node.level, key: node.data.label.split(' ')[0] })
  }
}

watch(
  () => props.data,
  v => {
    total.value = 0
    tree.val = [
      {
        label: `All (0)`,
        children: []
      }
    ]
    formatData(v, tree.val[0])
  },
  {
    immediate: true,
    deep: true
  }
)
</script>
<template>
  <el-card class="tree-card mb-15" shadow="never">
    <el-scrollbar height="260px">
      <el-tree
        :data="tree.val"
        :props="defaultProps"
        :highlight-current="true"
        :expand-on-click-node="false"
        :default-expand-all="true"
        @node-click="treeNodeClick"
      />
    </el-scrollbar>
  </el-card>
</template>

<style scoped>
.tree-card {
  user-select: none;
  height: 300px;
}
</style>
