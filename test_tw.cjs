const postcss = require('postcss');
const tailwindcss = require('tailwindcss');

const config = {
  content: [{ raw: '<div class="border-main/10 bg-main text-main"></div>' }],
  theme: {
    extend: {
      colors: {
        main: 'rgba(var(--color-text-main), <alpha-value>)'
      }
    }
  }
};

postcss([tailwindcss(config)])
  .process('@tailwind utilities;', { from: undefined })
  .then(result => {
    console.log(result.css);
  });
