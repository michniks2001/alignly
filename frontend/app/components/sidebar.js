"use client";

import {
  Box,
  Stack,
  Button,
  Divider,
  Typography,
  CircularProgress,
} from "@mui/material";
import Link from "next/link";
import { useEffect, useState } from "react";
import { app, auth } from "../firebase";
import { useRouter } from "next/navigation";
import { useTheme } from "@mui/material/styles";

const Sidebar = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const theme = useTheme();

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const handleLogout = async () => {
    await auth.signOut();
    router.push("/login");
  };

  const buttonStyle = {
    color: theme.palette.text.primary,
    backgroundColor: "transparent",
    "&:hover": {
      backgroundColor: theme.palette.action.hover,
    },
    justifyContent: "flex-start",
    textTransform: "none",
    fontWeight: "normal",
    fontSize: "1rem",
    padding: "10px 16px",
    borderRadius: "8px",
    width: "100%",
  };

  if (loading) {
    return (
      <Box
        p={2}
        justifyItems='center'
        height='100vh'
        width='20%'
        borderRight={`1px solid ${theme.palette.divider}`}
      >
        <Stack spacing={2}>
          <Typography variant='h4' color='primary'>
            Alignly
          </Typography>
          <Divider />
          <CircularProgress />
        </Stack>
      </Box>
    );
  }

  return (
    <Box
      height='100vh'
      width='20%'
      borderRight={`1px solid ${theme.palette.divider}`}
      bgcolor={theme.palette.background.paper}
      p={2}
    >
      <Stack spacing={2}>
        <Typography variant='h4' color='primary'>
          Alignly
        </Typography>
        <Divider />

        {user ? (
          <Stack spacing={1}>
            <Link href='/notepad' passHref style={{ textDecoration: "none" }}>
              <Button sx={buttonStyle}>New Note</Button>
            </Link>
            <Button sx={buttonStyle}>Profile</Button>

            <Link href='/events' passHref style={{ textDecoration: "none" }}>
              <Button sx={buttonStyle}>Your Calendar</Button>
            </Link>
            <Button onClick={handleLogout} sx={buttonStyle}>
              Logout
            </Button>
          </Stack>
        ) : (
          <Stack spacing={1}>
            <Link href='/register' passHref style={{ textDecoration: "none" }}>
              <Button sx={buttonStyle}>Register</Button>
            </Link>
            <Link href='/login' passHref style={{ textDecoration: "none" }}>
              <Button sx={buttonStyle}>Login</Button>
            </Link>
          </Stack>
        )}
      </Stack>
    </Box>
  );
};

export default Sidebar;
