import Card from "@/components/shared/Card";
import CardBody from "@/components/shared/CardBody";
import CardHeader from "@/components/shared/CardHeader";

function Legend() {
  return (
    <Card>
      <CardHeader>Legend</CardHeader>
      <CardBody>
        <div className="p-4">
          <code>!command [required-argument] (optional-argument)</code>
        </div>
      </CardBody>
    </Card>
  );
}

export default Legend;
