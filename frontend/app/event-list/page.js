"use client";

import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { auth, db } from "../firebase";
import { collection, query, where, getDocs } from "firebase/firestore";

const EventListPage = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const theme = useTheme();

  useEffect(() => {
    const fetchEvents = async () => {
      const user = auth.currentUser;
      if (user) {
        try {
          const eventsRef = collection(db, "events");
          const q = query(eventsRef, where("userId", "==", user.uid));
          const querySnapshot = await getDocs(q);
          const eventList = querySnapshot.docs.map((doc) => ({
            id: doc.id,
            ...doc.data(),
          }));
          setEvents(eventList);
        } catch (error) {
          console.error("Error fetching events: ", error);
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  if (loading) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box
      sx={{
        p: 3,
        backgroundColor: theme.palette.background.default,
        minHeight: "100vh",
      }}
    >
      <Typography
        variant='h4'
        sx={{ mb: 3, color: theme.palette.primary.main }}
      >
        Your Events
      </Typography>
      {events.length > 0 ? (
        <List>
          {events.map((event) => (
            <ListItem
              key={event.id}
              sx={{
                backgroundColor: theme.palette.background.paper,
                mb: 2,
                borderRadius: 1,
              }}
            >
              <ListItemText
                primary={event.title}
                secondary={new Date(event.date).toLocaleDateString()}
                primaryTypographyProps={{ color: theme.palette.text.primary }}
                secondaryTypographyProps={{
                  color: theme.palette.text.secondary,
                }}
              />
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography sx={{ color: theme.palette.text.secondary }}>
          No events found.
        </Typography>
      )}
    </Box>
  );
};

export default EventListPage;
