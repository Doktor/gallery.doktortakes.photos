const config = require('./webpack.common.js');
const merge = require('webpack-merge');


module.exports = merge(config, {
  mode: 'development',

  stats: {
    colors: true,
  },

  watch: true,
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000
  },
});
