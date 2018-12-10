<template>
    <div>
        <div class="container">
        <h3>Spark job configurator</h3>
        <p>
          Find the best configuration to deploy your Spark application in YARN in cluster-mode.
          This project is based on <a target="_blank" href="http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet">Anthony Shipman</a>'s article which I give my thanks.
        </p>
        </div>
        <div class="container">
          <div class="row">
            <form class="col-sm">
                <h5>Cluster</h5>
                <v-cluster v-model="cluster"/>
                <h5>Executors</h5>
                <div class="form-group row">
                  <label class="col-sm-8 col-form-label col-form-label-sm">Executors Per Node</label>
                  <div class="col-sm-4">
                    <input v-model="config.executorsPerNode" class="form-control form-control-sm" type="number" min = 1 step = 1>
                  </div>
                </div>
            </form>
            <form class="col-sm">
                <h5>Change with care</h5>
                <div class="form-group row">
                    <label class="col-sm-8 col-form-label col-form-label-sm">Memory Overhead Coefficient</label>
                    <div class="col-sm-4">
                        <input v-model="config.memoryOverheadCoefficient" class="form-control form-control-sm" type="number" min=0>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-8 col-form-label col-form-label-sm">Executor Memory Upper Bound (GB)</label>
                    <div class="col-sm-4">
                        <input v-model="config.executorMemoryUpperBoundGB" class="form-control form-control-sm" type="number" min=0>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-8 col-form-label col-form-label-sm">Executor Core Upper Bound</label>
                    <div class="col-sm-4">
                        <input v-model="config.executorCoreUpperBound" class="form-control form-control-sm" type="number" min=0>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-8 col-form-label col-form-label-sm">OS Reserved Cores</label>
                    <div class="col-sm-4">
                        <input v-model="config.osReservedCores" class="form-control form-control-sm" type="number" min=0>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-8 col-form-label col-form-label-sm">OS Reserved Memory (GB)</label>
                    <div class="col-sm-4">
                        <input v-model="config.osReservedMemoryGB" class="form-control form-control-sm" type="number" min=0>
                    </div>
                </div>
                <div class="form-group row">
                    <label class="col-sm-8 col-form-label col-form-label-sm">Parallelism Per Core</label>
                    <div class="col-sm-4">
                        <input v-model="config.parallelismPerCore" class="form-control form-control-sm" type="number" min=0>
                    </div>
                </div>
            </form>
          </div>
        </div>
        <hr class="style1"/>
        <div class="container">
          <div class="row">
          <div class="col-sm">
            <h5>Spark configuration </h5>
            <table class="table table-sm">
              <tbody>
                <tr><td>spark.executor.instances</td><td>{{spark.executorInstances}}</td></tr>
                <tr><td>spark.yarn.executor.memoryOverhead </td><td>{{spark.yarnExecutorMemoryOverhead}}</td></tr>
                <tr><td>spark.executor.memory</td><td>{{spark.executorMemory}}</td></tr>
                <tr><td>spark.yarn.driver.memoryOverhead </td><td>{{spark.yarnDriverMemoryOverhead}}</td></tr>
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
    --spark.yarn.executor.memoryOverhead {{spark.yarnExecutorMemoryOverhead}} \
    --spark.executor.memory {{spark.executorMemory}} \
    --spark.yarn.driver.memoryOverhead {{spark.yarnDriverMemoryOverhead}} \
    --spark.driver.memory {{spark.driverMemory}} \
    --spark.executor.cores {{spark.executorCores}} \
    --spark.driver.cores {{spark.driverCores}} \
    --spark.default.parallelism {{spark.defaultParallelism}} \
    &lt;your jar&gt;
               </code></pre>
          </div>
        </div>
        </div>
        <div class="container">
          <h5>External references</h5>
          <ul>
              <li><a target="_blank" href="https://spark.apache.org/docs/latest/running-on-yarn.html">https://spark.apache.org/docs/latest/running-on-yarn.html</a></li>
              <li><a target="_blank" href="http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet">http://c2fo.io/c2fo/spark/aws/emr/2016/07/06/apache-spark-config-cheatsheet</a></li>
          </ul>
        </div>
    </div>
</template>

<script>
export default {

  data () {
    return {
      cluster: {
        tabIndex: 1,
        nodes: 30,
        nodeMemory: 60,
        nodeCores: 8,
        ec2: 'r3.xlarge'
      },
      config: {
        executorsPerNode: 5,
        memoryOverheadCoefficient: 0.1,
        executorMemoryUpperBoundGB: 64,
        executorCoreUpperBound: 5,
        osReservedMemoryGB: 1,
        osReservedCores: 1,
        parallelismPerCore: 2
      }
    }
  },
  computed: {
    spark () {
      var nodes = null
      var nodeMemoryGB = null
      var nodeCores = null

      if (this.cluster.tabIndex === 0) {
        nodes = this.cluster.nodes
        nodeMemoryGB = this.cluster.nodeMemory
        nodeCores = this.cluster.nodeCores
      } else {
        nodes = this.cluster.nodes
        nodeMemoryGB = this.$store.state.emr[this.cluster.ec2]['yarn.nodemanager.resource.memory-mb']['default'] / 1024
        nodeCores = this.$store.state.ec2[this.cluster.ec2]['cpu']
      }
      console.log('nodes=' + nodes + ' nodeMemoryGB=' + nodeMemoryGB + ' nodeCores=' + nodeCores)

      var availableMemory = nodeMemoryGB - this.config.osReservedMemoryGB
      var availableCores = nodeCores - this.config.osReservedCores
      var executorInstances = nodes * this.config.executorsPerNode - 1

      var totalMemoryPerExecutor = Math.floor(availableMemory / this.config.executorsPerNode)
      var overheadMemoryPerExecutor = Math.ceil(totalMemoryPerExecutor * this.config.memoryOverheadCoefficient)
      var memoryPerExecutor = totalMemoryPerExecutor - overheadMemoryPerExecutor
      var coresPerExecutor = Math.floor(availableCores / this.config.executorsPerNode)
      // var unusedMemoryPerNode = availableMemory - totalMemoryPerExecutor * this.config.executorsPerNode
      // var unusedCoresPerNode = availableCores - coresPerExecutor * this.config.executorsPerNode

      var yarnExecutorMemoryOverhead = overheadMemoryPerExecutor * 1024
      var executorMemory = memoryPerExecutor
      var yarnDriverMemoryOverhead = yarnExecutorMemoryOverhead
      var driverMemory = executorMemory
      var executorCores = coresPerExecutor
      var driverCores = executorCores
      var defaultParallelism = executorInstances * executorCores * this.config.parallelismPerCore

      return {
        executorInstances: executorInstances,
        yarnExecutorMemoryOverhead: yarnExecutorMemoryOverhead + 'G',
        executorMemory: executorMemory,
        yarnDriverMemoryOverhead: yarnDriverMemoryOverhead + 'G',
        driverMemory: driverMemory,
        executorCores: executorCores,
        driverCores: driverCores,
        defaultParallelism: defaultParallelism
      }
    }
  }
}
</script>
