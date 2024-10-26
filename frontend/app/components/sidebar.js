import { Box, Stack, Button, Divider, Typography } from "@mui/material";
import Link from "next/link";

const Sidebar = () => {
  return (
    <Box
      height='100vh'
      width='20%'
      borderRight='black solid 1px'
      justifyItems='center'
      p={2}
    >
      <Stack spacing={2}>
        <Typography variant='h3'>Alignly</Typography>
        <Divider />
        <Link style={{ width: "100%" }} href='/register'>
          <Button
            disableRipple
            disableFocusRipple
            sx={{
              "&:hover": {
                backgroundColor: "transparent",
              },
              "&:focus": {
                outline: "none",
              },
            }}
          >
            Register
          </Button>
        </Link>
        <Link style={{ width: "100%" }} href='/register'>
          <Button
            disableRipple
            disableFocusRipple
            variant='text'
            sx={{
              "&:hover": {
                backgroundColor: "transparent",
              },
              "&:focus": {
                outline: "none",
              },
            }}
          >
            Login
          </Button>
        </Link>
      </Stack>
    </Box>
  );
};

export default Sidebar;
