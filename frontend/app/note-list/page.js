"use client";

import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  IconButton,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { collection, query, where, getDocs } from "firebase/firestore";
import { auth, db } from "../firebase";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import { useRouter } from "next/navigation";

const NoteListPage = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const theme = useTheme();
  const router = useRouter();

  useEffect(() => {
    const fetchNotes = async () => {
      const user = auth.currentUser;
      if (user) {
        try {
          const notesRef = collection(db, user.uid);
          const q = query(notesRef);
          const querySnapshot = await getDocs(q);
          const noteList = querySnapshot.docs.map((doc) => ({
            id: doc.id,
            ...doc.data(),
          }));
          setNotes(noteList);
        } catch (error) {
          console.error("Error fetching notes: ", error);
        } finally {
          setLoading(false);
        }
      } else {
        setLoading(false);
      }
    };

    fetchNotes();
  }, []);

  const handleEdit = (noteId) => {
    router.push(`/notepad?id=${noteId}`);
  };

  const handleDelete = async (noteId) => {
    // Implement delete functionality here
    console.log("Delete note:", noteId);
  };

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
        Your Notes
      </Typography>
      {notes.length > 0 ? (
        <List>
          {notes.map((note) => (
            <ListItem
              key={note.id}
              sx={{
                backgroundColor: theme.palette.background.paper,
                mb: 2,
                borderRadius: 1,
              }}
            >
              <ListItemText
                primary={note.title}
                secondary={note.content.substring(0, 100) + "..."}
                primaryTypographyProps={{ color: theme.palette.text.primary }}
                secondaryTypographyProps={{
                  color: theme.palette.text.secondary,
                }}
              />
              <IconButton onClick={() => handleEdit(note.id)}>
                <EditIcon />
              </IconButton>
              <IconButton onClick={() => handleDelete(note.id)}>
                <DeleteIcon />
              </IconButton>
            </ListItem>
          ))}
        </List>
      ) : (
        <Typography sx={{ color: theme.palette.text.secondary }}>
          No notes found. Start creating some!
        </Typography>
      )}
    </Box>
  );
};

export default NoteListPage;
