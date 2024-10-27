"use client";

import React, { useState, useEffect } from "react";
import { Stack, TextField } from "@mui/material";
import { debounce } from "lodash";

const NotepadPage = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  const handleSave = () => {
    // Implement your save logic here
    console.log("Saving note:", { title, content });
    // You might want to call an API or use a state management solution here
  };

  const debouncedSave = debounce(handleSave, 3000);

  useEffect(() => {
    debouncedSave();
    return () => debouncedSave.cancel();
  }, [title, content]);

  return (
    <Stack
      spacing={2}
      sx={{ width: "100%", maxWidth: 600, margin: "auto", padding: 2 }}
    >
      <TextField
        label='Note Title'
        variant='outlined'
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        fullWidth
      />
      <TextField
        label='Note Content'
        variant='outlined'
        multiline
        rows={4}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        fullWidth
      />
    </Stack>
  );
};

export default NotepadPage;
