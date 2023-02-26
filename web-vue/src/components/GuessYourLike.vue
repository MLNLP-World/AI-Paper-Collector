<script setup lang="ts">
const props = defineProps(['loading', 'result'])
const emits = defineEmits(['search-guess'])
const search = (searchContent: string): void => {
  emits('search-guess', searchContent)
}
</script>

<template>
  <el-card class="mb-15 box-card" shadow="never">
    <template #header>
      <div class="card-header">
        <span>Guess your like</span>
      </div>
    </template>
    <div class="guess-like-list" v-loading="props.loading">
      <ol v-show="props.result.length > 0">
        <li v-for="(itm, index) in props.result" :key="index" class="mb-5">
          <el-link @click="search(itm)">{{ itm }}</el-link>
        </li>
      </ol>
      <el-empty
        v-show="props.result.length <= 0"
        description="No guess result"
        :image-size="50"
      ></el-empty>
    </div>
  </el-card>
</template>

<style scoped>
.guess-like-list ol {
  padding-left: 15px;
}
</style>
