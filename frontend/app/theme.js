"use client";

import { createTheme, CssBaseline, ThemeProvider } from "@mui/material";
import "@fontsource/open-sauce-sans";

const theme = createTheme({
  typography: {
    fontFamily: `'Open Sauce Sans', sans-serif`,
  },
  palette: {
    primary: {
      main: "#1C7C54",
    },
    secondary: {
      main: "#2A628F",
    },
    background: {
      default: "#FDFCDC",
      paper: "#FFF",
    },
    text: {
      primary: "#1E2019",
      secondary: "#444",
    },
  },
});

const Providers = ({ children }) => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
};

export default Providers;
