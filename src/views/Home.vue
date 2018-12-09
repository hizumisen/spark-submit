<template>
  <div class="home">
    <SparkSubmit msg="SparkSubmit"/>
  </div>
</template>

<script>
// @ is an alias to /src
import SparkSubmit from '@/components/SparkSubmit.vue'

export default {
  name: 'home',
  components: {
    SparkSubmit
  }
}
</script>
