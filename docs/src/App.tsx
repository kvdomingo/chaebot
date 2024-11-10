import "./App.css";
import { queryClient } from "@/lib/api.ts";
import { QueryClientProvider } from "@tanstack/react-query";
import Content from "./components/commands/Content";
import Footer from "./components/shared/Footer";
import Navbar from "./components/shared/Navbar";

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Navbar />
      <Content />
      <Footer />
    </QueryClientProvider>
  );
}

export default App;
