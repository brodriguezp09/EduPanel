module.exports = {
  content: [
    "../templates/**/*.html",
    "../../templates/**/*.html", // Apunta a la carpeta de templates principal
    "../../users/templates/**/*.html", // Apunta a las plantillas de la app users
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#e6f7f0",
          100: "#ccefe2",
          200: "#99dfc5",
          300: "#66cfaa",
          400: "#33bf8e",
          500: "#016E44", // Tu color base (Verde Irlanda)
          600: "#005e3a",
          700: "#004e30",
          800: "#003e26",
          900: "#002f1c",
          950: "#001f13",
        },
        neutral: {
          50: "#f7f7f7",
          100: "#e3e3e3",
          200: "#c8c8c8",
          300: "#a4a4a4",
          400: "#818181",
          500: "#666666",
          600: "#515151",
          700: "#444444",
          800: "#333333", // Tu color base (Fondo)
          900: "#2b2b2b",
          950: "#1a1a1a",
        },
        accent: {
          50: "#fffbeb",
          100: "#fef3c7",
          200: "#fde68a",
          300: "#fcd34d",
          400: "#FBBF24", // Color de acento
          500: "#f59e0b",
          600: "#d97706",
          700: "#b45309",
          800: "#92400e",
          900: "#78350f",
          950: "#451a03",
        },
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
