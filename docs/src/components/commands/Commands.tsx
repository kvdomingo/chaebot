import { Fragment } from "react";

import Card from "@/components/shared/Card";
import CardBody from "@/components/shared/CardBody";
import CardHeader from "@/components/shared/CardHeader";

interface CommandsProps {
  header: string;
  commands: {
    command: string;
    required?: string[];
    optional?: string[];
    description: string;
  }[];
}

function Commands({ header, commands }: CommandsProps) {
  return (
    <Card id={header.toLowerCase()}>
      <CardHeader>{header} commands</CardHeader>
      <CardBody>
        <ul>
          {commands.map((command, index) => (
            <Fragment key={command.command}>
              {index > 0 && <hr className="border-slate-600" />}
              <li className="p-4">
                <div className="grid grid-cols-4">
                  <div>
                    <code>
                      !{command.command}
                      {command.required?.map((req, i) => (
                        <Fragment key={req}>{` [${req}]`}</Fragment>
                      ))}
                      {command.optional?.map((opt, i) => (
                        <Fragment key={opt}>{` (${opt})`}</Fragment>
                      ))}
                    </code>
                  </div>
                  <div className="col-span-3">{command.description}</div>
                </div>
              </li>
            </Fragment>
          ))}
        </ul>
      </CardBody>
    </Card>
  );
}

export default Commands;
