import { Fragment } from "react";
import { Badge, Card, CardHeader, CardBody, Row, Col, ListGroup, ListGroupItem } from "reactstrap";
import PropTypes from "prop-types";

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

Commands.propTypes = {
  header: PropTypes.string.isRequired,
  commands: PropTypes.shape({
    command: PropTypes.string.isRequired,
    required: PropTypes.arrayOf(PropTypes.string),
    optional: PropTypes.arrayOf(PropTypes.string),
    description: PropTypes.arrayOf(PropTypes.string.isRequired),
  }).isRequired,
  labeledCommand: PropTypes.bool,
  labelColor: PropTypes.string,
  labelName: PropTypes.string,
};

export default Commands;
