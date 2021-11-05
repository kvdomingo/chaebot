import React from "react";
import Navbar from "./components/shared/Navbar";
import Footer from "./components/shared/Footer";
import Content from "./components/commands/Content";

export default function App() {
  return (
    <div>
      <Navbar />
      <Content />
      <Footer />
    </div>
  );
}
