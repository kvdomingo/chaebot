import React from "react";
import { Card, CardHeader, CardBody, ListGroup, ListGroupItem } from "reactstrap";

export default function Legend() {
  return (
    <Card className="my-3">
      <CardHeader>Legend</CardHeader>
      <CardBody>
        <ListGroup>
          <ListGroupItem>
            <code>!command|alias1|alias2 [required-argument] (optional-argument)</code>
          </ListGroupItem>
        </ListGroup>
      </CardBody>
    </Card>
  );
}
