import React, { useEffect, useState } from "react";
import FullCalendar from "@fullcalendar/react";
import timeGridPlugin from "@fullcalendar/timegrid";

export default function ScheduleCalendar() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // Fetch schedule from FastAPI backend
    fetch("http://127.0.0.1:8000/schedule")
      .then((res) => res.json())
      .then((data) => {
        // Convert backend JSON to FullCalendar format
        const formattedEvents = [];
        const dayMap = {
          "Mon": 1,
          "Tue": 2,
          "Wed": 3,
          "Thu": 4,
          "Fri": 5,
          "Sat": 6,
          "Sun": 0,
        };

        Object.entries(data).forEach(([day, items]) => {
          items.forEach((item) => {
            formattedEvents.push({
              title: `${item.type.toUpperCase()}: ${item.title}`,
              daysOfWeek: [dayMap[day]], // Mon=1, Sun=0
              startTime: item.start,
              endTime: item.end,
              backgroundColor:
                item.type === "class"
                  ? "#ef4444"
                  : item.type === "commitment"
                  ? "#000000"
                  : "#fbbf24",
              borderColor: "#ffffff",
            });
          });
        });

        setEvents(formattedEvents);
      });
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Weekly Schedule</h2>
      <FullCalendar
        plugins={[timeGridPlugin]}
        initialView="timeGridWeek"
        allDaySlot={false}
        events={events}
        height="auto"
      />
    </div>
  );
}