import { useEffect, useState } from "react";

import { AdvancedImage } from "@cloudinary/react";
import { fill } from "@cloudinary/url-gen/actions/resize";
import { max } from "@cloudinary/url-gen/actions/roundCorners";
import { Github } from "lucide-react";

import { cld } from "@/cloudinary";
import ButtonLink from "@/components/shared/ButtonLink";

import { commands as menuItems } from "../commands/Content";

const navLogo = cld.image("kvisualbot/avatar");
navLogo.resize(fill().height(60).width(60).gravity("face")).roundCorners(max());

export default function Navigation() {
  const [version, setVersion] = useState("");

  useEffect(() => {
    (async () => {
      const result = await fetch(
        "https://api.github.com/repos/kvdomingo/chaebot/tags",
        {
          headers: {
            Accept: "application/vnd.github.v3+json",
          },
        },
      );

      if (result.ok) {
        const data = await result.json();
        setVersion(data[0].name);
      } else {
        console.error(await result.text());
      }
    })();
  }, []);

  return (
    <nav className="flex place-content-between place-items-center px-8">
      <div className="flex items-center gap-4">
        <a href="/" className="flex items-center gap-4">
          <AdvancedImage cldImg={navLogo} className="rounded-[50%]" />
          <h1 className="mr-6 text-2xl ">ChaeBot</h1>
        </a>
        {menuItems.map(({ header }) => (
          <div key={header}>
            <a href={`#${header.toLowerCase()}`}>{header}</a>
          </div>
        ))}
      </div>

      <div className="flex items-center gap-4">
        <ButtonLink
          href="https://discord.com/api/oauth2/authorize?client_id=726835246892580865&permissions=256064&scope=bot"
          className="border-sky-500 text-sky-500 hover:bg-sky-500"
        >
          Add to Discord
        </ButtonLink>
        <ButtonLink
          href="https://discord.gg/jQ5dpeN"
          className="border-emerald-500 text-emerald-500 hover:bg-emerald-500"
        >
          Join Discord server
        </ButtonLink>
        <a
          href="https://github.com/kvdomingo/chaebot"
          rel="noopener noreferrer"
          target="_blank"
          className="rounded-[50%] bg-white p-1 transition-all duration-100 ease-in-out hover:brightness-125"
        >
          <Github size="1.5rem" className="text-slate-800" />
        </a>
        <pre className="text-neutral-500">{version}</pre>
      </div>
    </nav>
  );
}
