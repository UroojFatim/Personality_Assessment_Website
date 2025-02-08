/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './quiz/templates/quiz/**/*.html',  // Path to HTML files in the quiz folder
    './quiz/static/js/**/*.js',         // Path to JS files if any
    './quiz/static/css/**/*.css',       // Path to your CSS files
  ],
  theme: {
    extend: {
      
    },
  },
  plugins: [],
};