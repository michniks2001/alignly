import { Box, Input, Stack, TextField, Typography } from "@mui/material";
import MarkdownShortcutsExample from "../components/textpad";

const HomePage = () => {
  return (
    <Box p={5} width='80vw'>
      <Stack spacing={5}>
        <MarkdownShortcutsExample />
      </Stack>
    </Box>
  );
};

export default HomePage;
