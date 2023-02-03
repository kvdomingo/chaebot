import { Fragment } from "react";
import { Badge, Card, CardBody, CardHeader, Col, ListGroup, ListGroupItem, Row } from "reactstrap";

interface CommandsProps {
  header: string;
  commands: {
    command: string;
    required?: string[];
    optional?: string[];
    description: string;
  }[];
  labeledCommand?: boolean;
  labelColor?: string;
  labelName?: string;
}

function Commands({ header, commands, labeledCommand, labelColor, labelName }: CommandsProps) {
  return (
    <Card className="my-3" id={header.toLowerCase()}>
      <CardHeader>
        {labeledCommand && <Badge color={labelColor}>{labelName}</Badge>} {header} commands
      </CardHeader>
      <CardBody>
        <ListGroup>
          {commands.map((command, i) => (
            <ListGroupItem key={i}>
              <Row key={i}>
                <Col sm="4">
                  <code>
                    /{command.command}
                    {command.required?.map((req, i) => (
                      <Fragment key={i}>{` [${req}]`}</Fragment>
                    ))}
                    {command.optional?.map((opt, i) => (
                      <Fragment key={i}>{` (${opt})`}</Fragment>
                    ))}
                  </code>
                </Col>
                <Col sm="8">{command.description}</Col>
              </Row>
            </ListGroupItem>
          ))}
        </ListGroup>
      </CardBody>
    </Card>
  );
}

export default Commands;
