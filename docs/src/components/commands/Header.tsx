import Card from "@/components/shared/Card";
import CardBody from "@/components/shared/CardBody";
import CardHeader from "@/components/shared/CardHeader";

export default function Legend() {
  return (
    <Card>
      <CardHeader>
        <h1 className="text-4xl">Commands</h1>
      </CardHeader>
      <CardBody>
        <p className="p-4">
          Listed here are the commands for <b>HanniBot</b> that can be used within a
          server channel. The default prefix is <kbd>!</kbd>.
        </p>
      </CardBody>
    </Card>
  );
}
