module.exports = {
  baseUrl: process.env.NODE_ENV === 'production' ? '/spark-submit/' : '/'
  domain: process.env.NODE_ENV === 'production' ? 'hizumisen.gitlab.io' : 'localhost:8080'
}