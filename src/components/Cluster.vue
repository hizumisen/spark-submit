<style type="text/css">
    /*prevent bootstrap-vue css conflict*/
    .v-select.dropdown .dropdown-toggle::after {
        content: none;
    }
    .v-select.dropdown .form-control {
        height: inherit;
    }
    .v-select .dropdown-toggle .clear {
        visibility: hidden;
    }
    .v-select.form-control-sm {
        padding: 0;
    }
    .nav {
      margin-bottom: 1rem;
    }
</style>
<template>
    <b-tabs v-model="value.tabIndex">
        <b-tab title="Custom">
            <div class="form-group row">
                <label class="col-sm-8 col-form-label col-form-label-sm">Number of Nodes</label>
                   <div class="col-sm-4">
                       <input v-model="value.nodes" class="form-control form-control-sm" type="number" min = 1 step = 1>
                    </div>
               </div>
               <div class="form-group row">
                <label class="col-sm-8 col-form-label col-form-label-sm">Memory Per Node (GB)</label>
                   <div class="col-sm-4">
                       <input v-model="value.nodeMemory" class="form-control form-control-sm" type="number" min = 1 step = 1>
                    </div>
               </div>
               <div class="form-group row">
                <label class="col-sm-8 col-form-label col-form-label-sm">Cores Per Node</label>
                   <div class="col-sm-4">
                       <input v-model="value.nodeCores" class="form-control form-control-sm" type="number" min = 1 step = 1>
                    </div>
               </div>
        </b-tab>
        <b-tab title="AWS EMR" >
            <div class="form-group row">
              <label class="col-sm-8 col-form-label col-form-label-sm">Number of Nodes</label>
              <div class="col-sm-4">
                <input v-model="value.nodes" class="form-control form-control-sm" type="number" min = 1 step = 1>
              </div>
            </div>
            <div class="form-group row">
              <label class="col-sm-8 col-form-label col-form-label-sm">Instance type</label>
                 <div class="col-sm-4">
                     <v-select class="form-control-sm" v-model="value.ec2" :options="Object.keys($store.state.emr)" ></v-select>
                  </div>
             </div>
        </b-tab>
    </b-tabs>
</template>

<script>
export default {
  props: ['value'],
  methods: {
    update (key, value) {
      this.$emit('input', { ...this.value, [key]: value })
    }
  }
}
</script>
