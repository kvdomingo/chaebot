import Commands from "./Commands";
import Header from "./Header";
import Legend from "./Legend";
import main from "./Main.json";
import schedule from "./Schedule.json";

export const commands = [
  { header: "Main", commands: main },
  { header: "Schedule", commands: schedule },
];

function Content() {
  return (
    <div className="container my-4">
      <Header />
      <Legend />
      {commands.map(command => (
        <Commands {...command} key={command.header} />
      ))}
    </div>
  );
}

export default Content;
