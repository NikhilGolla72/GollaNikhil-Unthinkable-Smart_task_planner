import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import PlannerView from "./pages/PlannerView";

export default function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/planner/:id" element={<PlannerView/>}/>
      </Routes>
    </BrowserRouter>
  )
}
