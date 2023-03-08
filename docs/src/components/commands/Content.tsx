import { Container } from "reactstrap";
import Commands from "./Commands";
import Header from "./Header";
import Legend from "./Legend";
import main from "./Main.json";
import schedule from "./Schedule.json";
import subscriptions from "./Subscriptions.json";

export const commands = [
  { header: "Main", commands: main },
  { header: "Subscription", commands: subscriptions },
  { header: "Schedule", commands: schedule },
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
