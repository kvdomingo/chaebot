import { cld } from "@/cloudinary";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar.tsx";
import { Button } from "@/components/ui/button.tsx";
import { api } from "@/lib/api.ts";
import { fill } from "@cloudinary/url-gen/actions/resize";
import { max } from "@cloudinary/url-gen/actions/roundCorners";
import { SiGithub } from "@icons-pack/react-simple-icons";
import { useQuery } from "@tanstack/react-query";
import { commands as menuItems } from "../commands/Content";

const navLogo = cld.image("kvisualbot/avatar");
navLogo.resize(fill().height(60).width(60).gravity("face")).roundCorners(max());

export default function Navigation() {
  const query = useQuery({
    queryKey: ["tags"],
    queryFn: api.tags,
  });

  const version = query.data?.data[0].name ?? "";

  return (
    <nav className="flex place-content-between place-items-center px-8 py-4">
      <div className="flex items-center gap-4">
        <a href="/" className="flex items-center gap-4">
          <Avatar>
            <AvatarImage src={navLogo.toURL()} alt="HanniBot" />
            <AvatarFallback>HB</AvatarFallback>
          </Avatar>
          <h1 className="mr-6 text-2xl ">HanniBot</h1>
        </a>
        {menuItems.map(({ header }) => (
          <a key={header} href={`#${header.toLowerCase()}`}>
            <Button variant="ghost">{header}</Button>
          </a>
        ))}
      </div>

      <div className="flex items-center gap-4">
        <a
          href="https://discord.com/api/oauth2/authorize?client_id=726835246892580865&permissions=256064&scope=bot"
          rel="noopener noreferrer"
          target="_blank"
        >
          <Button variant="default">Add to Discord</Button>
        </a>
        <a
          href="https://github.com/kvdomingo/hannibot"
          rel="noopener noreferrer"
          target="_blank"
        >
          <SiGithub size="1.5rem" className="text-primary" />
        </a>
        <pre className="text-neutral-500">{version}</pre>
      </div>
    </nav>
  );
}
