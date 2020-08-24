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
    .fade-enter-active, .fade-leave-active {
      transition: opacity .2s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
      opacity: 0;
    }
</style>
<template>
    <div class="container">
      <div class="pb-2 mt-4 mb-2">
        <h1>Spark job configurator</h1>
      </div>
      <social-sharing
        url="https://hizumisen.gitlab.io/spark-submit/"
        title="spark-submit: a Spark job configurator"
        description="Find the best configuration to deploy your Spark applications in YARN in cluster-mode by optimizing your cluster resources."
        hashtags="spark"
        twitter-user="hizumisen"
        inline-template
        class="mb-4">
        <div>
            <network network="twitter" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','twitter']" size="lg"/></button></network>
            <network network="facebook" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','facebook']" size="lg"/></button></network>
            <network network="linkedin" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','linkedin']" size="lg"/></button></network>
            <network network="reddit" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','reddit']" size="lg"/></button></network>
            <network network="line" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','line']" size="lg"/></button></network>
            <network network="telegram" class="m-1"><button class="btn btn-outline-secondary" type="button"><font-awesome-icon :icon="['fab','telegram']" size="lg"/></button></network>
        </div>
      </social-sharing>
      <p>
        Find the best configuration to deploy your Spark applications in YARN in cluster-mode by optimizing your cluster resources.
        This project is based on <a target="_blank" href="http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet">Anthony Shipman</a>'s article which I give my thanks.
        This configuration is based on Spark 2.4 version.
      </p>
      <h3>Job configuration</h3>
      <p>
        Complete the forum below with your cluster specs and the number of executor you want to have for each node.
        If deploy your application in an AWS EMR cluster, you can directly specify the instance type and the number of nodes (the number of cores and memory of each node will be automatically derived from the instance type).
        The remaining parameters should be changed only if your application require particular configurations.
      </p>
      <div class="row">
        <div class="col-sm">
            <b-card
              title="Cluster"
              class="row"
            >
              <b-tabs v-model="cluster.tabIndex">
                <b-tab title="Custom">
                    <div class="form-group row mt-3">
                        <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Number of Nodes</label>
                           <div class="col-xs-12 col-sm-12 col-lg-5">
                               <b-form-input v-model="cluster.nodes" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodes.$invalid && null"></b-form-input>
                            </div>
                       </div>
                       <div class="form-group row">
                        <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Memory Per Node (MB)</label>
                           <div class="col-xs-12 col-sm-12 col-lg-5">
                               <b-form-input v-model="cluster.nodeMemory" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodeMemory.$invalid && null"></b-form-input>
                            </div>
                       </div>
                       <div class="form-group row">
                        <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Cores Per Node</label>
                           <div class="col-xs-12 col-sm-12 col-lg-5">
                               <b-form-input v-model="cluster.nodeCores" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodeCores.$invalid && null"></b-form-input>
                            </div>
                       </div>
                </b-tab>
                <b-tab title="AWS EMR" >
                    <div class="form-group row mt-3">
                      <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Number of Nodes</label>
                      <div class="col-xs-12 col-sm-12 col-lg-5">
                        <b-form-input v-model="cluster.nodes" class="form-control form-control-sm" type="number" :state="!$v.cluster.nodes.$invalid && null"></b-form-input>
                      </div>
                    </div>
                    <div class="form-group row">
                      <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">Instance type</label>
                         <div class="col-xs-12 col-sm-12 col-lg-5">
                             <v-select class="form-control-sm" v-model="cluster.ec2" :options="Object.keys($store.state).sort()" ></v-select>
                          </div>
                     </div>
                </b-tab>
              </b-tabs>
            </b-card>
            <b-card
              title="Executors"
              class="row"
            >
              <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The number of spark executor to run in each node of the cluster.'""/>
                  Executors Per Node
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                  <b-form-input v-model.number="config.executorsPerNode" class="form-control form-control-sm" type="number" :state="!$v.config.executorsPerNode.$invalid && null"></b-form-input>
                </div>
              </div>
            </b-card>
        </div>
        <div class="col-sm">
            <b-card
              title="Change with care"
              class="row h-100"
            >
            <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The percentage of memory off-heap memory to be allocated per executor.'""/>
                  Memory Overhead Coefficient
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                    <b-form-input v-model.number="config.memoryOverheadCoefficient" class="form-control form-control-sm" type="number" :state="!$v.config.memoryOverheadCoefficient.$invalid && null"></b-form-input>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The maximum amount of memory an executor can use.'""/>
                  Executor Memory Upper Bound (MB)
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                    <b-form-input v-model.number="config.executorMemoryUpperBoundMB" class="form-control form-control-sm" type="number" :state="!$v.config.executorMemoryUpperBoundMB.$invalid && null"></b-form-input>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The maximum amount of cores an executor can use.'""/>
                  Executor Core Upper Bound
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                    <b-form-input v-model.number="config.executorCoreUpperBound" class="form-control form-control-sm" type="number" :state="!$v.config.executorCoreUpperBound.$invalid && null"></b-form-input>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The number of cores that will be reserved for the OS for each node.'""/>
                  OS Reserved Cores
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                    <b-form-input v-model.number="config.osReservedCores" class="form-control form-control-sm" type="number" :state="!$v.config.osReservedCores.$invalid && null"></b-form-input>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The memory amount that will be reserved for the OS for each node.'""/>
                  OS Reserved Memory (MB)
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                    <b-form-input v-model.number="config.osReservedMemoryMB" class="form-control form-control-sm" type="number" :state="!$v.config.osReservedMemoryMB.$invalid && null"></b-form-input>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-xs-12 col-sm-12 col-lg-7 col-form-label col-form-label-sm">
                  <font-awesome-icon icon="question-circle" v-b-popover.hover="'The level of parallelism per allocated core.'""/>
                  Parallelism Per Core
                </label>
                <div class="col-xs-12 col-sm-12 col-lg-5">
                    <b-form-input v-model.number="config.parallelismPerCore" class="form-control form-control-sm" type="number" :state="!$v.config.parallelismPerCore.$invalid && null"></b-form-input>
                </div>
            </div>
          </b-card>
        </div>
      </div>
      <div class="mt-4 mb-4">
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
      <div class="mt-4 mb-2">
        <h3>Computed configuration</h3>
        <p>
          Below you can find computed configuration
        </p>
        <table class="table table-sm">
          <tbody>
            <tr v-for="(value, key) in spark.configurations"><td>{{ key }}</td><td>{{ value }}</td></tr>
          </tbody>
        </table>
        <h6>Spark submit command</h6>
        <div>
          <p class="text-light bg-dark p-2 w-100 rounded"><code>{{spark.sparkSubmitCommand}}</code></p>
          <b-button variant="outline-primary" v-on:click="copyCommandToClipboard">
            <font-awesome-icon icon="copy"/>
          </b-button>
          <transition name="fade"><span v-if="clipboardMsgShow" class="ml-2 text-success">Copied to clipboard</span></transition>
        </div>
      </div>
      <div>
        <h3>External references</h3>
        <ul>
            <li><a target="_blank" href="https://spark.apache.org/docs/2.4.0/running-on-yarn.html">https://spark.apache.org/docs/2.4.0/running-on-yarn.html</a></li>
            <li><a target="_blank" href="http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet">http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet</a></li>
        </ul>
      </div>
      <vue-cookie-accept-decline
          :ref="'myPanel1'"
          :elementId="'myPanel1'"
          :debug="false"
          :position="'bottom-left'"
          :type="'floating'"
          :disableDecline="false"
          :transitionName="'slideFromBottom'"
          :showPostponeButton="true"
          @status="cookieStatus"
          @clicked-accept="cookieClickedAccept"
          @clicked-decline="cookieClickedDecline"
          @clicked-postpone="cookieClickedPostpone"
          @removed-cookie="cookieRemovedCookie">
          <div slot="postponeContent">
              &times;
          </div>
          <div slot="message">
              We use cookies to ensure you get the best experience on our website. <a href="https://cookiesandyou.com/" target="_blank">Learn More...</a>
          </div>
          <div slot="declineContent">
              OPT OUT
          </div>
          <div slot="acceptContent">
              GOT IT!
          </div>
        </vue-cookie-accept-decline>
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
        nodeMemory: 60000,
        nodeCores: 8,
        ec2: 'r5.2xlarge'
      },
      config: {
        executorsPerNode: 5,
        memoryOverheadCoefficient: 0.1,
        executorMemoryUpperBoundMB: 64*1024,
        executorCoreUpperBound: 5,
        osReservedMemoryMB: 1024,
        osReservedCores: 1,
        parallelismPerCore: 2
      },
      clipboardMsgShow: false,
      status: null
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
    cookieStatus (status) {
        this.status = status
    },
    cookieClickedAccept () {
        this.status = 'accept'
    },
    cookieClickedDecline () {
        this.status = 'decline'
    },
    cookieClickedPostpone () {
        this.status = 'postpone'
    },
    cookieRemovedCookie () {
        this.status = null
        this.$refs.myPanel1.init()
    },
    removeCookie () {
        this.$refs.myPanel1.removeCookie()
    },
    copyCommandToClipboard: function (event) {
      const context = this
      this.$copyText(this.spark.sparkSubmitCommand).then(function (e) {
        context.clipboardMsgShow = true
      }, function (e) {
        alert('Can not copy')
        console.log(e)
      })
    },
    fadeClipboardMessage() {
      setTimeout(() => (
        this.clipboardMsgShow = false
      ), 2000);
    }
  },
  watch: {
    clipboardMsgShow: 'fadeClipboardMessage',
  },
  computed: {
    spark () {
      function getClusterConfig(cluster, store) {
        if (cluster.tabIndex === 0) {
          return {
            nodes: cluster.nodes,
            nodeMemoryMB: cluster.nodeMemory,
            nodeCores: cluster.nodeCores
          }
        } else {
          return {
            nodes: cluster.nodes,
            nodeMemoryMB: store.state[cluster.ec2]['yarn.nodemanager.resource.memory-mb'],
            nodeCores: store.state[cluster.ec2]['cpu']
          }
        }
      }
      function getSparkSubmitCommand(configurations) {
        const sparkSubmitCommandConfigurations = Array.from(Object.entries(configurations), ([key, value]) => '--conf ' + key + ' ' + value).join(' ')
        return 'spark-submit --class <your-class> ' + sparkSubmitCommandConfigurations + ' <your-jar>'
      }
      
      var errors = []
      if(this.$v.$invalid) {
        errors.push('Invalid configuration.')
        const configurations = {
            'spark.executor.instances': 0,
            'spark.executor.memory': '0m',
            'spark.yarn.am.memoryOverhead': '0m',
            'spark.driver.memory': '0m',
            'spark.executor.cores': 0,
            'spark.driver.cores': 0,
            'spark.default.parallelism': 0
        }
        return {
          errors: errors,
          configurations: configurations,
          sparkSubmitCommand: getSparkSubmitCommand(configurations)
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

        const configurations = {
            'spark.executor.instances': executorInstances,
            'spark.executor.memory': executorMemory + 'm',
            'spark.yarn.am.memoryOverhead': memoryOverhead + 'm',
            'spark.driver.memory': driverMemory + 'm',
            'spark.executor.cores': executorCores,
            'spark.driver.cores': driverCores,
            'spark.default.parallelism': defaultParallelism
        }
        return {
          errors: errors,
          configurations: configurations,
          sparkSubmitCommand: getSparkSubmitCommand(configurations)
        }
      }
    }
  }
}
</script>
