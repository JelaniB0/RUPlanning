import React from "react";
import ScheduleCalendar from "./scheduleCalendar";
import './App.css'; // keep this if you want your styles
import './calendar.css'; // or './calendar.css'

function App() {
  return (
    <div className="App">
      <h1 className="text-2xl font-bold text-center my-4">RUPlanning</h1>
      <ScheduleCalendar />
    </div>
  );
}

export default App;