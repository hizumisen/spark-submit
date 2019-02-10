var webpack = require('webpack');

module.exports = {
  baseUrl: process.env.NODE_ENV === 'production' ? '/spark-submit/' : '/',
  chainWebpack: config => {
    config.optimization.delete('splitChunks')
  }
}