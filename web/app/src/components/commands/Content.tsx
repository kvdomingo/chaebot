import { Container } from "reactstrap";
import Legend from "./Legend";
import Header from "./Header";
import Commands from "./Commands";
import main from "./Main.json";
import subscriptions from "./Subscriptions.json";
import mama from "./Mama.json";

export const commands = [
  { header: "Main", commands: main },
  { header: "Subscription", commands: subscriptions },
  { header: "MAMA 2022", commands: mama },
];

function Content() {
  return (
    <Container className="my-5">
      <Header />
      <Legend />
      {commands.map((command, i) => (
        <Commands {...command} key={i} />
      ))}
    </Container>
  );
}

export default Content;
