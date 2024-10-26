import { Box, Button, Divider, Typography } from "@mui/material";

const Sidebar = () => {
  return (
    <Box height='100vh' width='15%'>
      <Typography component='h2'>Alignly</Typography>
      <Divider />
      <Button color='blue'>New Page</Button>
    </Box>
  );
};

export default Sidebar;
