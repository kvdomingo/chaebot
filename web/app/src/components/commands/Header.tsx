import { Card, CardHeader, CardBody } from "reactstrap";

export default function Legend() {
  return (
    <Card className="my-3">
      <CardHeader>
        <h1 className="display-5">Commands</h1>
      </CardHeader>
      <CardBody>
        Listed here are the slash commands for <b>KVISUALBOT</b> that can be used within a server channel.
      </CardBody>
    </Card>
  );
}
