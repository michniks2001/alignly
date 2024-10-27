"use client";

import { Box, Button, Typography, Paper, Grid, Container } from "@mui/material";
import { auth } from "./firebase";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useTheme } from "@mui/material/styles";
import EditNoteIcon from "@mui/icons-material/EditNote";
import FormatListBulletedIcon from "@mui/icons-material/FormatListBulleted";
import CloudSyncIcon from "@mui/icons-material/CloudSync";

export default function Home() {
  const [user, setUser] = useState(null);
  const theme = useTheme();

  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setUser(user);
    });

    return () => unsubscribe();
  }, []);

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100%",
        backgroundColor: theme.palette.background.default,
      }}
    >
      <Container maxWidth='lg'>
        <Box sx={{ pt: 8, pb: 6 }}>
          <Typography
            variant='h2'
            align='center'
            color='primary'
            gutterBottom
            sx={{ fontWeight: "bold", mb: 4 }}
          >
            Welcome to Alignly
          </Typography>
          <Typography
            variant='h5'
            align='center'
            color='text.secondary'
            paragraph
            sx={{ mb: 4 }}
          >
            Your personal markdown editor for organized thoughts and ideas.
          </Typography>
          <Box sx={{ mt: 4, display: "flex", justifyContent: "center" }}>
            <Link href={user ? "/dashboard" : "/register"} passHref>
              <Button
                variant='contained'
                size='large'
                sx={{
                  backgroundColor: theme.palette.primary.main,
                  color: theme.palette.background.paper,
                  "&:hover": {
                    backgroundColor: theme.palette.primary.dark,
                  },
                  textTransform: "none",
                  fontSize: "1.2rem",
                  padding: "10px 30px",
                  borderRadius: "8px",
                }}
              >
                {user ? "Go to Dashboard" : "Get Started"}
              </Button>
            </Link>
          </Box>
        </Box>

        <Grid container spacing={4} sx={{ mt: 4 }}>
          <Grid item xs={12} sm={4}>
            <Paper
              elevation={3}
              sx={{
                p: 3,
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <EditNoteIcon
                sx={{ fontSize: 60, color: theme.palette.primary.main, mb: 2 }}
              />
              <Typography
                variant='h5'
                component='h3'
                align='center'
                gutterBottom
              >
                Markdown Support
              </Typography>
              <Typography align='center'>
                Write your notes in Markdown for easy formatting and
                organization.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Paper
              elevation={3}
              sx={{
                p: 3,
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <FormatListBulletedIcon
                sx={{ fontSize: 60, color: theme.palette.primary.main, mb: 2 }}
              />
              <Typography
                variant='h5'
                component='h3'
                align='center'
                gutterBottom
              >
                Task Management
              </Typography>
              <Typography align='center'>
                Create and manage tasks within your notes for better
                productivity.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Paper
              elevation={3}
              sx={{
                p: 3,
                height: "100%",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <CloudSyncIcon
                sx={{ fontSize: 60, color: theme.palette.primary.main, mb: 2 }}
              />
              <Typography
                variant='h5'
                component='h3'
                align='center'
                gutterBottom
              >
                Cloud Sync
              </Typography>
              <Typography align='center'>
                Your notes are automatically synced across all your devices.
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
