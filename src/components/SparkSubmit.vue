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
    <div class="container">
        <div class="pb-2 mt-4 mb-2 border-bottom">
          <h1>Spark job configurator</h1>
        </div>
        <social-sharing
          url="https://hizumisen.gitlab.io/spark-submit/"
          title="spark-submit: a Spark job configurator"
          description="Find the best configuration to deploy your Spark applications in YARN in cluster-mode by optimizing your cluster resources."
          hashtags="spark"
          twitter-user="hizumisen"
          inline-template>
          <div>
              <network network="twitter" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','twitter']" size="lg"/></button></network>
              <network network="facebook" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','facebook']" size="lg"/></button></network>
              <network network="linkedin" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','linkedin']" size="lg"/></button></network>
              <network network="reddit" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','reddit']" size="lg"/></button></network>
              <network network="line" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','line']" size="lg"/></button></network>
              <network network="telegram" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','telegram']" size="lg"/></button></network>
          </div>
        </social-sharing>
        <p class="mt-4">
          Find the best configuration to deploy your Spark applications in YARN in cluster-mode by optimizing your cluster resources.
          This project is based on <a target="_blank" href="http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet">Anthony Shipman</a>'s article which I give my thanks.
        </p>
        <div class="row">
          <form class="col-sm">
              <h5>Cluster</h5>
              <b-tabs v-model="cluster.tabIndex">
                <b-tab title="Custom">
                    <div class="form-group row">
                        <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Number of Nodes</label>
                           <div class="col-xs-12 col-sm-12 col-lg-5">
                               <b-form-input v-model="cluster.nodes" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodes.$invalid"></b-form-input>
                            </div>
                       </div>
                       <div class="form-group row">
                        <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Memory Per Node (GB)</label>
                           <div class="col-xs-12 col-sm-12 col-lg-5">
                               <b-form-input v-model="cluster.nodeMemory" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodeMemory.$invalid"></b-form-input>
                            </div>
                       </div>
                       <div class="form-group row">
                        <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Cores Per Node</label>
                           <div class="col-xs-12 col-sm-12 col-lg-5">
                               <b-form-input v-model="cluster.nodeCores" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodeCores.$invalid"></b-form-input>
                            </div>
                       </div>
                </b-tab>
                <b-tab title="AWS EMR" >
                    <div class="form-group row">
                      <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Number of Nodes</label>
                      <div class="col-xs-12 col-sm-12 col-lg-5">
                        <b-form-input v-model="cluster.nodes" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodes.$invalid"></b-form-input>
                      </div>
                    </div>
                    <div class="form-group row">
                      <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Instance type</label>
                         <div class="col-xs-12 col-sm-12 col-lg-5">
                             <v-select class="form-control-sm" v-model="cluster.ec2" :options="Object.keys($store.state.emr)" ></v-select>
                          </div>
                     </div>
                </b-tab>
            </b-tabs>
              <h5>Executors</h5>
              <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The number of spark executor to run in each node of the cluster.'""/>
                  Executors Per Node
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                  <b-form-input v-model.number="config.executorsPerNode" class="form-control form-control-sm" type="number" :state="!$v.config.executorsPerNode.$invalid"></b-form-input>
                </div>
              </div>
          </form>
          <form class="col-sm">
              <h5>Change with care</h5>
              <div class="form-group row">
                  <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                    <font-awesome-icon icon="question-circle" v-b-popover.hover="'The percentage of memory off-heap memory to be allocated per executor.'""/>
                    Memory Overhead Coefficient
                  </label>
                  <div class="col-xs-12 col-sm-12 col-lg-5">
                      <b-form-input v-model.number="config.memoryOverheadCoefficient" class="form-control form-control-sm" type="number" :state="!$v.config.memoryOverheadCoefficient.$invalid"></b-form-input>
                  </div>
              </div>
              <div class="form-group row">
                  <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                    <font-awesome-icon icon="question-circle" v-b-popover.hover="'The maximum amount of memory an executor can use.'""/>
                    Executor Memory Upper Bound (MB)
                  </label>
                  <div class="col-xs-12 col-sm-12 col-lg-5">
                      <b-form-input v-model.number="config.executorMemoryUpperBoundMB" class="form-control form-control-sm" type="number" :state="!$v.config.executorMemoryUpperBoundMB.$invalid"></b-form-input>
                  </div>
              </div>
              <div class="form-group row">
                  <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                    <font-awesome-icon icon="question-circle" v-b-popover.hover="'The maximum amount of cores an executor can use.'""/>
                    Executor Core Upper Bound
                  </label>
                  <div class="col-xs-12 col-sm-12 col-lg-5">
                      <b-form-input v-model.number="config.executorCoreUpperBound" class="form-control form-control-sm" type="number" :state="!$v.config.executorCoreUpperBound.$invalid"></b-form-input>
                  </div>
              </div>
              <div class="form-group row">
                  <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                    <font-awesome-icon icon="question-circle" v-b-popover.hover="'The number of cores that will be reserved for the OS for each node.'""/>
                    OS Reserved Cores
                  </label>
                  <div class="col-xs-12 col-sm-12 col-lg-5">
                      <b-form-input v-model.number="config.osReservedCores" class="form-control form-control-sm" type="number" :state="!$v.config.osReservedCores.$invalid"></b-form-input>
                  </div>
              </div>
              <div class="form-group row">
                  <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                    <font-awesome-icon icon="question-circle" v-b-popover.hover="'The memory amount that will be reserved for the OS for each node.'""/>
                    OS Reserved Memory (MB)
                  </label>
                  <div class="col-xs-12 col-sm-12 col-lg-5">
                      <b-form-input v-model.number="config.osReservedMemoryMB" class="form-control form-control-sm" type="number" :state="!$v.config.osReservedMemoryMB.$invalid"></b-form-input>
                  </div>
              </div>
              <div class="form-group row">
                  <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                    <font-awesome-icon icon="question-circle" v-b-popover.hover="'The level of parallelism per allocated core.'""/>
                    Parallelism Per Core
                  </label>
                  <div class="col-xs-12 col-sm-12 col-lg-5">
                      <b-form-input v-model.number="config.parallelismPerCore" class="form-control form-control-sm" type="number" :state="!$v.config.parallelismPerCore.$invalid"></b-form-input>
                  </div>
              </div>
          </form>
        </div>
        <div>
          <b-btn v-b-toggle.collapse1 variant="danger" v-if="spark.errors.length">
            Errors <span class="badge badge-light">{{spark.errors.length}}</span>
          </b-btn>
          <b-btn v-b-toggle.collapse1 variant="success" v-else>
            No errors
          </b-btn>
          <b-collapse id="collapse1" class="mt-2" v-if="spark.errors.length">
            <b-card no-body bg-variant="danger">
              <ul class="list-group list-group-flush">
                <li v-for="error in spark.errors" class="list-group-item list-group-item-danger">{{ error }}</li>
              </ul>
            </b-card>
          </b-collapse>
        </div>
        <div class="row pb-2 pt-2 mt-4 mb-2 border-top">
        <div class="col-sm">
          <h5>Spark configuration </h5>
          <table class="table table-sm">
            <tbody>
              <tr><td>spark.executor.instances</td><td>{{spark.executorInstances}}</td></tr>
              <tr><td>spark.executor.memory</td><td>{{spark.executorMemory}}</td></tr>
              <tr><td>spark.yarn.am.memoryOverhead </td><td>{{spark.memoryOverhead}}</td></tr>
              <tr><td>spark.driver.memory</td><td>{{spark.driverMemory}}</td></tr>
              <tr><td>spark.executor.cores</td><td>{{spark.executorCores}}</td></tr>
              <tr><td>spark.driver.cores</td><td>{{spark.driverCores}}</td></tr>
              <tr><td>spark.default.parallelism</td><td>{{spark.defaultParallelism}}</td></tr>
            </tbody>
          </table>
        </div>
        <div class="col-sm">
          <h5>Spark submit </h5>
             <pre><code>
spark-submit \
    --&lt;your class&gt; \
    --spark.executor.instances {{spark.executorInstances}} \
    --spark.executor.memory {{spark.executorMemory}} \
    --spark.yarn.am.memoryOverhead {{spark.memoryOverhead}} \
    --spark.driver.memory {{spark.driverMemory}} \
    --spark.executor.cores {{spark.executorCores}} \
    --spark.driver.cores {{spark.driverCores}} \
    --spark.default.parallelism {{spark.defaultParallelism}} \
    &lt;your jar&gt;
             </code></pre>
        </div>
      </div>
      <div>
        <h5>External references</h5>
        <ul>
            <li><a target="_blank" href="https://spark.apache.org/docs/2.4.0/running-on-yarn.html">https://spark.apache.org/docs/2.4.0/running-on-yarn.html</a></li>
            <li><a target="_blank" href="http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet">http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet</a></li>
        </ul>
      </div>
    </div>
</template>

<script>
import { validationMixin } from "vuelidate"
import { integer, numeric, decimal, minValue, maxValue } from 'vuelidate/lib/validators'

export default {
  data () {
    return {
      cluster: {
        tabIndex: 0,
        nodes: 30,
        nodeMemory: 60,
        nodeCores: 8,
        ec2: 'r3.xlarge'
      },
      config: {
        executorsPerNode: 5,
        memoryOverheadCoefficient: 0.1,
        executorMemoryUpperBoundMB: 64*1024,
        executorCoreUpperBound: 5,
        osReservedMemoryMB: 1024,
        osReservedCores: 1,
        parallelismPerCore: 2
      }
    }
  },
  mixins: [
    validationMixin
  ],
  validations: {
    cluster: {
      nodes : { integer, minValue:minValue(1) },
      nodeMemory : { integer, minValue:minValue(1) },
      nodeCores : { integer, minValue:minValue(1) },
    },
    config: {
      executorsPerNode: { integer, minValue:minValue(1) },
      memoryOverheadCoefficient: { decimal, minValue:minValue(0), maxValue:maxValue(1) },
      executorMemoryUpperBoundMB: { integer, minValue:minValue(0) },
      executorCoreUpperBound: { integer, minValue:minValue(0) },
      osReservedMemoryMB: { integer, minValue:minValue(0) },
      osReservedCores: { integer, minValue:minValue(0) },
      parallelismPerCore: { integer, minValue:minValue(1) }
    }
  },
  methods: {
    status(validation) {
      return {
        success: validation.$error,
        danger: validation.$dirty
      }
    }
  },
  computed: {
    spark () {
      function getClusterConfig(cluster, store) {
        if (cluster.tabIndex === 0) {
          return {
            nodes: cluster.nodes,
            nodeMemoryMB: cluster.nodeMemory * 1024,
            nodeCores: cluster.nodeCores
          }
        } else {
          return {
            nodes: cluster.nodes,
            nodeMemoryMB: store.state.emr[cluster.ec2]['yarn.nodemanager.resource.memory-mb']['default'],
            nodeCores: store.state.ec2[cluster.ec2]['cpu']
          }
        }
      }
      
      var errors = []
      if(this.$v.$invalid) {
        errors.push('Invalid configuration')
        return {
          errors: errors,
          executorInstances: 0,
          memoryOverhead: '0m',
          executorMemory: '0m',
          driverMemory: '0m',
          executorCores: 0,
          driverCores: 0,
          defaultParallelism: 0
        }
      }else{
        const cluter = getClusterConfig(this.cluster, this.$store)
        const availableMemoryMB = cluter.nodeMemoryMB - this.config.osReservedMemoryMB
        const availableCores = cluter.nodeCores - this.config.osReservedCores
        const executorInstances = cluter.nodes * this.config.executorsPerNode - 1

        if (availableMemoryMB <= 0)
          errors.push('The memory reserved for the OS (' + this.config.osReservedMemoryMB + ') is greater than the one available (' + cluter.nodeMemoryMB + ').')
        if (availableCores <= 0)
          errors.push('The cores reserved for the OS (' + this.config.osReservedCores + ' core) is greater than the one availables (' + cluter.nodeCores + ' cores).')
        
        const totalMemoryPerExecutor = Math.floor(availableMemoryMB / this.config.executorsPerNode)
        if (totalMemoryPerExecutor <= 0)
          errors.push('A lot of executors configured (' + this.config.executorsPerNode + ' executors) for the memory available per node (' + availableMemoryMB + 'MB).')
        const memoryOverheadPerExecutor = Math.ceil(totalMemoryPerExecutor * this.config.memoryOverheadCoefficient)
        const memoryPerExecutor = totalMemoryPerExecutor - memoryOverheadPerExecutor
        if (memoryPerExecutor <= 0)
          errors.push('The memory reserved for each executor (' + totalMemoryPerExecutor + 'MB) is greater than the one available (' + memoryOverheadPerExecutor + 'MB are reserved for overhead).')
        const coresPerExecutor = Math.floor(availableCores / this.config.executorsPerNode)
        if (coresPerExecutor <= 0)
          errors.push('A lot of executors configured (' + this.config.executorsPerNode + ' executors) for the cores available per node (' + availableCores + ' cores).')
        // const unusedMemoryPerNode = availableMemory - totalMemoryPerExecutor * this.config.executorsPerNode
        // const unusedCoresPerNode = availableCores - coresPerExecutor * this.config.executorsPerNode

        const memoryOverhead = memoryOverheadPerExecutor
        const executorMemory = memoryPerExecutor
        const driverMemory = executorMemory
        const executorCores = coresPerExecutor
        const driverCores = executorCores
        const defaultParallelism = executorInstances * executorCores * this.config.parallelismPerCore

        return {
          errors: errors,
          executorInstances: executorInstances,
          memoryOverhead: memoryOverhead + 'm',
          executorMemory: executorMemory + 'm',
          driverMemory: driverMemory + 'm',
          executorCores: executorCores,
          driverCores: driverCores,
          defaultParallelism: defaultParallelism
        }
      }
    }
  }
}
</script>
