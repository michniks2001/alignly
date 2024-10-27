"use client";

import React, { useState } from "react";
import {
  TextField,
  Button,
  Box,
  Typography,
  Paper,
  InputAdornment,
  Link,
} from "@mui/material";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "../firebase";
import EmailIcon from "@mui/icons-material/Email";
import LockIcon from "@mui/icons-material/Lock";
import { useTheme } from "@mui/material/styles";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const theme = useTheme();

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const userCredentials = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );
      if (userCredentials.user.emailVerified) {
        alert("Login Successful!");
      } else {
        alert("Verify your email before logging in");
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        width: "100vw",
        backgroundColor: theme.palette.background.default,
      }}
    >
      <Paper
        elevation={3}
        sx={{
          padding: 4,
          width: "100%",
          maxWidth: 400,
          borderRadius: 2,
          backgroundColor: theme.palette.background.paper,
        }}
      >
        <Typography
          variant='h4'
          component='h1'
          gutterBottom
          align='center'
          sx={{ mb: 4, fontWeight: "bold", color: theme.palette.primary.main }}
        >
          Login to Alignly
        </Typography>
        <form onSubmit={handleLogin}>
          <TextField
            label='Email'
            variant='outlined'
            fullWidth
            margin='normal'
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position='start'>
                  <EmailIcon color='primary' />
                </InputAdornment>
              ),
            }}
            sx={{ mb: 2 }}
          />
          <TextField
            label='Password'
            type='password'
            variant='outlined'
            fullWidth
            margin='normal'
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position='start'>
                  <LockIcon color='primary' />
                </InputAdornment>
              ),
            }}
            sx={{ mb: 3 }}
          />
          {error && (
            <Typography color='error' sx={{ mb: 2 }}>
              {error}
            </Typography>
          )}
          <Button
            type='submit'
            variant='contained'
            fullWidth
            sx={{
              backgroundColor: theme.palette.primary.main,
              color: theme.palette.background.paper,
              "&:hover": {
                backgroundColor: theme.palette.primary.dark,
              },
              textTransform: "none",
              fontSize: "1rem",
              padding: "10px 0",
              borderRadius: "8px",
            }}
          >
            Login
          </Button>
        </form>
        <Typography
          variant='body2'
          align='center'
          sx={{ mt: 3, color: theme.palette.text.secondary }}
        >
          Don't have an account?{" "}
          <Link
            href='/register'
            color='secondary'
            sx={{ textDecoration: "none" }}
          >
            Sign up
          </Link>
        </Typography>
      </Paper>
    </Box>
  );
};

export default Login;
