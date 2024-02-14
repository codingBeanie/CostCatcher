/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,vue}"],
  theme: {
    extend: {
      colors: {
        "primary": {
          300: "#192224",
          200: "#66888F",
          100: "#ABC0C4"
        },
        "secondary": {
          300: "#8F4300",
          200: "#E06900",
          100: "#FFBE85"
        },
        "light": {
          300: "#DAE0E7",
          200: "#E7EBEF",
          100: "#F3F5F7"
        },
        "highlight": {
          400: "#FFC2C2",
          300: "#E6F4CD",
          200: "#FFDEC2",
          100: "#BEEFED"
        }
      },
      plugins: []
    }
  }
}