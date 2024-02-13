/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,vue}"],
  theme: {
    extend: {
      colors: {
        "primary": {
          300: "#2A323C",
          200: "#708299",
          100: "#E7EBEF"
        },
        "secondary": {
          300: "#8F4300",
          200: "#E06900",
          100: "#FFBE85"
        }
      },
      plugins: []
    }
  }
}