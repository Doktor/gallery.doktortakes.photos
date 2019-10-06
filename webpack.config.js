const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = {
  mode: 'development',

  context: __dirname,

  entry: {
    browser: path.resolve('src/browser.js'),
    editor: path.resolve('src/editor.js'),
  },

  output: {
    path: path.resolve('./static/bundles/'),
    filename: '[name].[hash].js',
  },

  stats: {
    colors: true,
  },

  plugins: [
    new BundleTracker({
      filename: './src/webpack-stats.json',
    }),
    new VueLoaderPlugin(),
  ],

  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {
          compilerOptions: {
            whitespace: 'condense',
          },
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.s[ac]ss$/,
        use: ['style-loader', 'css-loader', 'sass-loader'],
      },
    ],
  },

  resolve: {
    alias: {
      vue: 'vue/dist/vue.js',
    },
  },

  watch: true,
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000
  }
};
