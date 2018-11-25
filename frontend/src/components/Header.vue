<template>
  <v-layout row>
    <v-avatar>
      <img class="logo" src="./../../static/hippo.png" alt="Avatar">
    </v-avatar>
    <v-toolbar-title class="mt-2"> SSE Semantic Search Engine </v-toolbar-title>
  </v-layout>
</template>

<script>
export default {
  name: 'app-header'
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
 .logo{
   height : 40px;
 }
</style>
