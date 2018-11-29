path = require('path');

module.exports = {
  entry: './url_shortener/www/static/www/js/index.js',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.less$/,
        use: [
          {
            loader: "style-loader"
          },
          {
            loader: "css-loader"
          },
          {
            loader: "less-loader"
          }
        ]
      },
    {
        test: /\.(pdf|jpg|png|gif|svg|ico)$/,
        use: [
          {
            loader: 'url-loader'
          },
        ]
    },
    ]
  },
  output: {
    path: path.resolve(__dirname, 'url_shortener/www/static/www/src'),
    filename: 'js/bundle.min.js'
  },
};
