"use client";

import { Box, Stack, Typography } from "@mui/material";
import MarkdownShortcutsExample from "./components/textpad";

export default function Home() {
  return (
    <Box height='100vh' display='flex' flexDirection='row'>
      <Stack p={5}>
        <Typography
          alignContent='center'
          justifyContent='center'
          textAlign='center'
          variant='h2'
        >
          Alignly
        </Typography>
        <MarkdownShortcutsExample />
      </Stack>
    </Box>
  );
}
