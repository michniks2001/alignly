"use client";

import React from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { Box, Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";

const EventsPage = () => {
  const theme = useTheme();

  const handleDateClick = (arg) => {
    alert("Date click! " + arg.dateStr);
  };

  const handleEventClick = (arg) => {
    alert("Event click! " + arg.event.title);
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        width: "100%",
        backgroundColor: theme.palette.background.default,
      }}
    >
      <Typography variant='h4' sx={{ p: 2, color: theme.palette.primary.main }}>
        Event Calendar
      </Typography>
      <Box
        sx={{
          flexGrow: 1,
          p: 2,
          "& .fc": {
            height: "100%",
            fontFamily: theme.typography.fontFamily,
          },
          "& .fc-toolbar-title": {
            color: theme.palette.text.primary,
          },
          "& .fc-button": {
            backgroundColor: theme.palette.primary.main,
            "&:hover": {
              backgroundColor: theme.palette.primary.dark,
            },
          },
          "& .fc-day": {
            backgroundColor: theme.palette.background.paper,
          },
          "& .fc-day-today": {
            backgroundColor: theme.palette.action.selected,
          },
        }}
      >
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView='dayGridMonth'
          headerToolbar={{
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,timeGridDay",
          }}
          buttonText={{
            today: "Today",
            month: "Month",
            week: "Week",
            day: "Day",
          }}
          events={[
            { title: "Event 1", date: "2023-06-01" },
            { title: "Event 2", date: "2023-06-15" },
          ]}
          dateClick={handleDateClick}
          eventClick={handleEventClick}
          height='100%'
        />
      </Box>
    </Box>
  );
};

export default EventsPage;
